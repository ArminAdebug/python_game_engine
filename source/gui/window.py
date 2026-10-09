# pylint: disable=no-name-in-module
from typing import TYPE_CHECKING

from PyQt6.QtCore import QTimer, QEvent
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QMenu,
    QLayout,
    QTreeWidgetItem,
    QListWidgetItem,
    QListWidget,
    QDoubleSpinBox,
    QPushButton
)

from source.gui.window_ui import Ui_MainWindow
from source.gui.inspector import Ui_Form as inspectorUi
from source.gui.transform_ui import Ui_Form as transformUi

from source.game_engine import GameEngine
from source.math import (
    Vector3,
    Quaternion
)
from source.logging import Logger

from source.components import (
    Transform,
    Sprite,
    Script
)

if TYPE_CHECKING:
    from source.object.scene import Scene
    from source.object.gameobject import GameObject


class Window(QMainWindow):
    """app main window and GUI
    """

    def __init__(self, engine: GameEngine):
        """setup app GUI

        Args:
            engine (GameEngine): object of Game Engine
        """

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.engine = engine

        # setup directx screen
        directx_window = QWindow.fromWinId(engine.directx_window.get_hwnd())
        container = QWidget.createWindowContainer(directx_window)
        layout = QVBoxLayout(self.ui.screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        self.timer = QTimer()

        self.ui.play_button.clicked.connect(
            lambda: self.engine.run_game(self.timer))

        self.ui.pause_button.clicked.connect(self.engine.exit_loop)

        self.update_hierarchy_tree()

        self.ui.hierarchy_tree.itemSelectionChanged.connect(
            self.onSelectionChanged)

        self.inspector_data = {"inspector": None,
                               "transform": None,
                               "object": None}
        self.inspector = None

        self.engine.ui_update_signal.signal.connect(self.update_ui_signal)

        self.ui_changing = False

        self.show()

    def update_ui_signal(self):
        if self.ui_changing > 0:
            self.ui_changing -= 0.0001
            return

        self.update_hierarchy_tree()

        if self.inspector_data["inspector"]:
            self._update_transform_ui(
                self.inspector_data["transform"], self.inspector_data["object"])

    def _update_transform_ui(self, transformui: transformUi, game_object: "GameObject"):

        transformui.x_position.setValue(game_object.transform.position.x)
        transformui.y_position.setValue(game_object.transform.position.y)
        transformui.z_position.setValue(game_object.transform.position.z)

        transformui.x_rotation.setValue(game_object.transform.rotation.x)
        transformui.y_rotation.setValue(game_object.transform.rotation.y)
        transformui.z_rotation.setValue(game_object.transform.rotation.z)

        transformui.x_scale.setValue(game_object.transform.scale.x)
        transformui.y_scale.setValue(game_object.transform.scale.y)
        transformui.z_scale.setValue(game_object.transform.scale.z)

    def _update_engine_transform(self):

        Logger.log_test("j")
        self.ui_changing = 1

        self.inspector_data["object"].transform.position = Vector3(
            self.inspector_data["transform"].x_position.value(),
            self.inspector_data["transform"].y_position.value(),
            self.inspector_data["transform"].z_position.value(),
        )

        self.inspector_data["object"].transform.rotation = Quaternion.euler(
            self.inspector_data["transform"].x_rotation.value(),
            self.inspector_data["transform"].y_rotation.value(),
            self.inspector_data["transform"].z_rotation.value(),
        )

        self.inspector_data["object"].transform.scale = Vector3(
            self.inspector_data["transform"].x_scale.value(),
            self.inspector_data["transform"].y_scale.value(),
            self.inspector_data["transform"].z_scale.value(),
        )

    def update_hierarchy_tree(self):
        """update hierarchy tree items"""

        scenes: dict[str, list[GameObject]] = {
            scene.name: scene.get_game_objects() for scene in self.engine.scenes}

        for name, objects in scenes.items():
            item = QTreeWidgetItem()
            item.setText(0, name)

            self.ui.hierarchy_tree.addTopLevelItem(item)
            for obj in objects:
                item2 = QTreeWidgetItem(item)
                item2.setText(0, obj.name)

    def onSelectionChanged(self):
        try:
            selected = self.ui.hierarchy_tree.selectedItems()

            if not selected:
                return

            item = selected[0]

            panel = QWidget()
            self.inspector = inspectorUi()
            self.inspector.setupUi(panel)

            self.inspector_data["inspector"] = self.inspector

            if not item.parent():
                return

            self.setupAddComponent(self.inspector.add_component_button)

            scene: Scene = [
                s for s in self.engine.scenes if s.name == item.parent().text(0)][0]
            game_object = scene.search_game_object(item.text(0))[0]

            self.inspector_data["object"] = game_object
            self.inspector.object_name.setText(game_object.name)
            for component in game_object.all_components():
                match component:
                    case Transform():
                        self._add_transform_ui(self.inspector.components)
                    case Script():
                        pass
                    case Sprite():
                        pass
                    case _:
                        Logger.log_error(
                            f"unknown component for inspector ui <{component}>")

            self.ui.inspector_dock.setWidget(panel)

        except Exception as e:
            Logger.log_exception(e)

    def _add_transform_ui(self, list_widget: QListWidget):
        widget = QWidget()

        transform = transformUi()
        transform.setupUi(widget)

        self.inspector_data["transform"] = transform
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())

        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

        inputs = [
            transform.x_position,
            transform.y_position,
            transform.z_position,
            transform.x_rotation,
            transform.y_rotation,
            transform.z_rotation,
            transform.x_scale,
            transform.y_scale,
            transform.z_scale,
        ]
        try:
            for i in inputs:
                i.installEventFilter(self)
                i.lineEdit().textEdited.connect(self._update_engine_transform)
                i.lineEdit().installEventFilter(self)

        except Exception as e:
            Logger.log_exception(e)

    def setupAddComponent(self, button : QPushButton):
        """connecting button to components list
        """
        menu = QMenu(self)

        menu.addAction("Transform")
        menu.addAction("Mesh Renderer")
        menu.addAction("Box Collider")
        menu.addAction("Rigidbody")

        button.clicked.connect(
            lambda: menu.exec(
                button.mapToGlobal(
                    button.rect().bottomLeft()
                )
            )
        )

    def _delete_layout(self, layout: QLayout):
        layout.deleteLater()

    def eventFilter(self, obj, event : QEvent):
        if isinstance(obj, QDoubleSpinBox):

            if event.type() in [QEvent.Type.FocusIn,]:
                pass
                #self._update_engine_transform()

            if event.type() == QEvent.Type.FocusOut:
                self._update_engine_transform()
                self.ui_changing = 0

        return super().eventFilter(obj, event)

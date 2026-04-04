from test import b, wr

c = b.wrt()

original = wr()

c : type[original]

c()
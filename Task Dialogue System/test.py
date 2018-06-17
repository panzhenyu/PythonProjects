class A:
    def __init__(self, a):
        self.a = a


class B:
    def __init__(self):
        self.pos = None

    def add(self, a):
        self.pos = a

a1 = A(1)
b = B()
b.add(a1)
a1.a = 3
print(b.pos.a)
a1 = A(2)
print(b.pos.a)

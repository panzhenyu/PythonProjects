class A:
    def __init__(self, x):
        self.x = x

    def __mul__(self, o):
        return A(self.x * o.x)

a1 = A(1)
a2 = A(2)
a3 = a1*a2
print(a3.x)
# test for super

class A(object):
    def f(self):
        print("A.f()")


class B(object):
    def f(self):
        print("B.f()")


class C(B, A):
    def f(self):
        print("C.f()")

    def testF(self):
        super(C, self).f()
        super(C, self).f()


c = C()
c.testF()

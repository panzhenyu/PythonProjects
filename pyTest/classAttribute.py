class Fib(object):
    def __init__(self):
        self.a, self.b = 1, 0

    def __iter__(self):
        return self

    def next(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 0
            while n >= 0:
                n -= 1
                a, b = b, a+b
            return a
        if isinstance(n, slice):
            result = []
            start = n.start
            stop = n.stop
            counter = -1
            a, b = 1, 0
            while True:
                a, b = b, a+b
                counter += 1
                if counter >= stop:
                    break
                if counter >= start:
                    if counter < stop:
                        result.append(a)
            return result

    def __call__(self):
        print("this is Fibonacci sequence test !")

    def __str__(self):
        return "this is Fibonacci sequence test !"
    __repr__ = __str__


def fun():
    pass


f = Fib()
print(Fib()[0])
print(Fib()[0:9])
print(callable(f))
f()
print(f)
print(callable(fun))
print(callable(int))
print(int('12'))
print(callable('int'))

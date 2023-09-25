class TProgon:
    a = []
    b = []
    c = []
    d = []
    z = []
    alpha = []
    beta = []
    yn = []

    def CalcZ(self):
        N = len(self.a)

        self.alpha.append(-self.c[0] / self.a[0])
        self.beta.append(self.d[0] / self.a[0])
        for n in range(1, N):
            self.alpha.append(-(self.c[n]) / (self.a[n] + self.b[n] * self.alpha[n - 1]))
            self.beta.append((self.d[n] - self.b[n] * self.beta[n - 1]) / (self.a[n] + self.b[n] * self.alpha[n - 1]))

        self.z.append(
            (self.d[N - 1] - self.b[N - 1] * self.beta[N - 2]) / (self.a[N - 1] + self.b[N - 1] * self.alpha[N - 2]))
        for n in range(N - 1, 0, -1):
            self.z[n] = self.alpha[n] * self.z[n + 1] + self.beta[n]


class TSpline:
    def __init__(self, xn, yn):
        self.N = len(xn)
        self.xn = xn
        self.yn = yn

    def h(self, n):
        return self.xn[n + 1] - self.xn[n]

    def mu(self, n):
        return self.h(n - 1) / (self.h(n - 1) + self.h(n))

    def la(self, n):
        return 1 - self.mu(n)

    def Build(self, m0, mN):
        # if len(self.yn) == len(self.xn):
        #     return

        self.Progon = TProgon()
        self.Progon.a = [0] * self.N
        self.Progon.b = [0] * self.N
        self.Progon.c = [0] * self.N
        self.Progon.d = [0] * self.N
        self.Progon.z = [0] * self.N
        for n_ in range(1, self.N - 1):
            self.Progon.a[n_] = 2.0
            self.Progon.b[n_] = self.la(n_)
            self.Progon.c[n_] = self.mu(n_)
            self.Progon.d[n_] = 3.0 * (self.mu(n_) * (self.yn[n_ + 1] - self.yn[n_])) / self.h(n_) + self.la(n_) * (
                    self.yn[n_] - self.yn[n_ - 1] / self.h(n_ - 1))

        self.Progon.a[0] = 2
        self.Progon.a[self.N - 1] = 2

        self.Progon.b[0] = 0
        self.Progon.b[self.N - 1] = 0

        self.Progon.c[0] = 0
        self.Progon.c[self.N - 1] = 0

        self.Progon.d[0] = 2 * m0
        self.Progon.d[self.N - 1] = 2 * mN

        self.Progon.CalcZ()

    def CalcSpline(self, x):
        n = 0
        for n in range(0, self.N - 2):
            if self.xn[n] <= x < self.xn[n + 1]:
                break
            n += 1

        t = (x - self.xn[n]) / self.h(n)
        return self.yn[n] * (1 - t) * (1 - t) * (1 + 2 * t) + self.yn[n+1] * t * t * (3 - 2 * t) + self.Progon.z[
            n] * self.h(n) * t * (1 - t) * (1 - t) - self.Progon.z[n + 1] * self.h(n) * t * t * (1 - t)


def int_input():
    ls = input().split()
    if len(ls) == 0:
        return
    for i in range(len(ls)):
        ls[i] = int(ls[i])
    return ls


if __name__ == '__main__':
    x_arr = int_input()
    y_arr = int_input()
    x_arr.insert(2, 1.25)
    y_arr.insert(2, 15.1)
    Spline = TSpline(x_arr, y_arr)
    Spline.Build(1, 7)
    print(round(Spline.CalcSpline(float(input())), 1))
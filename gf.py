import fire
from prettytable import PrettyTable
from sympy import *


class GF:
    def __init__(self, w):
        assert w in [3, 4, 8, 16, 32, 64]
        primitive_polynomial_dict = {
                3: 0b1011, # x^3 + x + 1
                4: 0b10011, # x^4 + x + 1
                8: (1 << 8) + 0b11101, # x^8 + x^4 + x^3 + x^2 + 1
                16: (1 << 16) + (1 << 12) + 0b1011, # x^16 + x^12 + x^3 + x + 1
                32: (1 << 32) + (1 << 22) + 0b111, # x^32 + x^22 + x^2 + x + 1
                64: (1 << 64) + 0b11011 # x^64 + x^4 + x^3 + x + 1
                }
        self.total = 1 << w
        self.max_no = self.total - 1
        self.primitive_polynomial = primitive_polynomial_dict[w]

    def __eq__(self, other):
        return self.total == other.total

    def add(self, a, b):
        #assert (a <= self.max_no) and (b <= self.max_no), f'Over the max {self.max_no}'
        return a ^ b

    def _divp(self, a):
        p = self.primitive_polynomial
        la = len(bin(a))
        lp = len(bin(p))
        if la > lp:
            d = p << (la - lp)
            c = self.add(a, d)
            return c
        elif la == lp:
            return self.add(a, p)
        else:
            return a

    def mul(self, a, b):
        #assert (a <= self.max_no) and (b <= self.max_no), f'Over the max {self.max_no}'
        s = list(bin(b))
        s.reverse()
        muls = []
        for i, c in enumerate(s[:-2]):
            if c == '1':
                sa = a << i
                muls.append(sa)
        res = 0
        for i in muls:
            res ^= i
        while res > self.max_no:
            res = self._divp(res)
        return res

    def div(self, a, b):
        mts = []
        for i in range(self.total):
            l = []
            for j in range(self.total):
                l.append(self.mul(i, j))
            mts.append(l)
        for i, v in enumerate(mts[b]):
            if v == a:
                return i


    def tables(self, flag='±'):
        nos = [f'{flag}']
        tb = PrettyTable()
        for i in range(self.total):
            nos.append(str(i))
        tb.field_names = nos
        for i in range(self.total):
            ls = [str(i)]
            for j in range(self.total):
                s = self.add(i, j)
                m = self.mul(i, j)
                d = self.div(i, j)
                flags = {'±': s, 'x': m, '/': d}
                ls.append(f'{flags[flag]}')
            tb.add_row(ls)
        print(tb)

class GFPolynomial:

    def __init__(self, *coeffs, gfs=3):
        poly = {}
        for i in range(len(coeffs)):
            monom = len(coeffs) - 1 - i
            poly[monom] = coeffs[i]
        self.poly = poly
        self.gf = GF(gfs)
        self.gfs = gfs
        print(f'GF(2^{gfs})')
        #self.gf.tables()
        #self.gf.tables(flag='x')

    def __repr__(self):
        x = Symbol('x')
        polys = 0
        for e, c in self.poly.items():
            polys += c * x ** e
        return f'多项式：{apart(polys)}\nLatex: {latex(polys)}'

    def __add__(self, other):
        assert self.gfs == other.gfs, '必须在同一伽罗瓦域内计算。'
        polys = max(max(self.poly), max(other.poly))
        res = []
        for i in range(polys + 1, -1, -1):
            a = self.poly.get(i, 0)
            b = other.poly.get(i, 0)
            c = self.gf.add(a, b)
            #print(i, a, b, c)
            res.append(c)
        return GFPolynomial(*res, gfs=self.gfs)

    def __mul__(self, other):
        assert self.gfs == other.gfs, '必须在同一伽罗瓦域内计算。'
        n = max(self.poly) + max(other.poly)
        res = [0] * (n+1)
        for ka, va in self.poly.items():
            for kb, vb in other.poly.items():
                k = ka + kb
                v = self.gf.mul(va, vb)
                res[-1-k] = self.gf.add(res[-1-k], v)
        return GFPolynomial(*res, gfs=self.gfs)

        

if __name__ == '__main__':
    a = GFPolynomial(1, 4, 7, 7, 0)
    b = GFPolynomial(3, 2, 0, 5)
    c = GFPolynomial(5, 0, 0, 0, 0, 0, 1, 0)
    print(f'a: {a}')
    print(f'b: {b}')
    print(f'c: {c}')
    print(a+b+c)
    d = a * b * c
    print(d)

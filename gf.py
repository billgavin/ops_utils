import fire
from prettytable import PrettyTable


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


if __name__ == '__main__':
    fire.Fire()

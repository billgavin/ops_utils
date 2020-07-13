import fire

class NumberTheory:

    thress = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]
    fours = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96]
    sevens = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210, 217, 224, 231, 238, 245, 252, 259, 266, 273, 280, 287, 294, 301, 308, 315, 322, 329, 336, 343, 350, 357, 364, 371, 378, 385, 392, 399, 406, 413, 420, 427, 434, 441, 448, 455, 462, 469, 476, 483, 490, 497, 504, 511, 518, 525, 532, 539, 546, 553, 560, 567, 574, 581, 588, 595, 602, 609, 616, 623, 630, 637, 644, 651, 658, 665, 672, 679, 686, 693, 700, 707, 714, 721, 728, 735, 742, 749, 756, 763, 770, 777, 784, 791, 798, 805, 812, 819, 826, 833, 840, 847, 854, 861, 868, 875, 882, 889, 896, 903, 910, 917, 924, 931, 938, 945, 952, 959, 966, 973, 980, 987, 994]
    nines = [9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99]

    # 判断回文数
    @classmethod
    def isPalindrome(cls, n):
        s = str(n)
        for i in range(len(s) // 2):
            if s[i] != s[-1-i]:
                return False
        return True

    # 判断偶数
    @classmethod
    def isOdd(cls, n):
        if n % 2 == 0:
            return True
        else:
            return False
    
    # 判断3的倍数
    @classmethod
    def isTriple(cls, n):
        s = 0
        for c in str(n):
            s += int(c)
        while len(str(s)) > 2:
            cls.isTriple(s)
        if s in cls.thress:
            return True
        else:
            return False

    # 判断4的倍数
    @classmethod
    def isFourth(cls, n):
        if n % 100 in cls.fours:
            return True
        else:
            return False

    # 判断5的倍数
    @classmethod
    def isFivefold(cls, n):
        if n % 5 in [0, 5]:
            return True
        else:
            return False

    # 判断6的倍数
    @classmethod
    def isSixth(cls, n):
        return cls.isOdd(n) and cls.isTriple(n)

    # 判断7的倍数
    @classmethod
    def _minus(cls, n):
        a, b = divmod(n, 1000)
        sub = abs(a - b)
        while len(str(sub)) > 3:
            cls._minus(sub)
        return sub
        

if __name__ == '__main__':
    fire.Fire()

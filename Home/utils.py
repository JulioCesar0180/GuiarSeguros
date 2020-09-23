from itertools import cycle


def validate_rut(value):
    try:
        rut = value.upper()
        rut = rut.replace("-", "").replace(".", "")
        num = rut[:-1]
        dv = rut[-1:]

        reversed_digits = map(int, reversed(str(num)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))
        res = (-s) % 11

        if str(res) == dv:
            return True
        elif dv == "K" and res == 10:
            return True
        else:
            return False
    except:
        return False
from fractions import Fraction

def display_fraction(a):
    if a != int(a):
        integer = a.numerator//a.denominator
        if integer == 0:
            integer = ''
        else:
            integer = str(integer) + ' '
        mod = a.numerator % a.denominator
        return f'{integer}{mod}/{a.denominator}'
    return a
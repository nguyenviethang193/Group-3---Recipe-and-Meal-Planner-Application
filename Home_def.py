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

def split_dict(input_dict):
    if len(input_dict) % 2 == 1:
        midpoint = len(input_dict) // 2 + 1
    else:
        midpoint  = len(input_dict) // 2
    
    dict1 = dict(list(input_dict.items())[:midpoint])
    dict2 = dict(list(input_dict.items())[midpoint:])
    
    return dict1, dict2
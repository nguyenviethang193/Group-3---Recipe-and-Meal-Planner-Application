from fractions import Fraction
import base64

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

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
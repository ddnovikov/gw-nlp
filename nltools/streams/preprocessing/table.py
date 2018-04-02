def standardize_ean(input_):
    if not input_.isdigit():
        return ''
    else:
        if len(input_) == 8 or len(input_) == 13:
            res = input_
        elif 8 < len(input_) < 13:
            return input_[:8]
        elif 13 < len(input_):
            return input_[:13]
        else:
            return input_


def standardize_inn(input_):
    if not input_.isdigit():
        return ''
    else:
        if len(input_) == 10 or len(input_) == 12:
            return input_
        elif 10 < len(input_) < 12:
            return input_[:10]
        elif 12 < len(input_):
            return input_[:12]
        else:
            return input_


def fix_digit_value(input_):
    if not input_.isdigit():
        return 0

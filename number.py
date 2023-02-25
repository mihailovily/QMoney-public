def checknum(number):
    if '--' in number:
        return False
    number = list(number)
    if number.count('(') >= 1 and number.count(')') >= 1:
        if number.index(')') < number.index('('):
            return False
    while '\t' in number:
        number.remove('\t')
    while ' ' in number:
        number.remove(' ')
    if number.count('(') > 1 or number.count(')') > 1 or number.count(')') != number.count('('):
        return False
    if number[-1] == '-' or number[0] == '-':
        return False
    if '--' in number:
        return False
    if number[0] == '8' or number[0] == '7 ':
        number = ['+'] + ['7'] + number[1:]
    if number[0] != '+':
        return False
    while '-' in number:
        number.remove('-')
    while '(' in number:
        number.remove('(')
    while ')' in number:
        number.remove(')')
    if (number[0] == '+' and len(number) != 12) or (number[0] != '+' and len(number) != 11):
        return False
    if number[0] == '+':
        for i in range(1, len(number)):
            if number[i].isdigit():
                pass
            else:
                return False
    if number[0] != '+':
        for i in range(len(number)):
            if number[i].isdigit():
                pass
            else:
                return False
    number1 = ''
    for i in range(1, len(number)):
        number1 += number[i]
    return number1



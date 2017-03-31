import os
import string
import sys

import requests

try:
    if sys.platform == 'linux':
        import getch as msvcrt
    else:
        import msvcrt
except ImportError:
    if sys.platform == 'win32':
        print('PLEASE INSTALL MSVCRT\npip install msvcrt')
    elif sys.platform == 'linux':
        print('PLEASE INSTALL GETCH\npip3 install getch')

printer = print
inputer = input

version = 1.6
colors = ['\033[91m', '\033[92m', '\033[97m', '\033[94m', '\033[96m', '\033[93m', '\033[95m', '\033[90m', '\033[90m',
          '\033[99m']


# colors = Red,Green,White,Blue,Cyan,Yellow,Magenta,Grey,Black,Default

def clear():
    try:
        os.system('clear')
    except:
        os.system('cls')


def hot_api():
    return version


def readcfg(file_name):
    settings = {}
    try:
        lines = open(file_name, 'r+')
    except:
        return {}
    for line in lines:
        line = line.split('<>')
        line[1] = line[1].split('\n')[0]
        settings.update({line[0]: line[1]})
    lines.close()
    return settings


def writecfg(file_name, library, check=True):
    if check:
        lines = readcfg(file_name)
        for every in lines:
            try:
                library[every]
            except KeyError:
                library[every] = lines[every]
    file = open(file_name, 'w+', encoding='utf-8')
    for every in library:
        file.write('%s<>%s\n' % (every, library[every]))
    file.close()
    return True


def print(string, is_new=True, color=9, clr=False, start=True, frame=False):
    if clr:
        clear()
        is_new = False
    if frame:
        string_ = string.split('\n')
        header = '┏' + '━' * (len(max(string_, key=len)) + 4) + '┓\n'
        header += '┃  ' + ' ' * len(max(string_, key=len)) + '  ┃\n'
        for every in string_:
            header += '┃  ' + every + ' ' * (len(max(string_, key=len)) - len(every)) + '  ┃\n'
        header += '┃  ' + ' ' * len(max(string_, key=len)) + '  ┃\n'
        header += '┗' + '━' * (len(max(string_, key=len)) + 4) + '┛'
        string = header
        is_new = True
    if is_new:
        sys.stdout.write('%s\n%s' % (colors[color], string))
    else:
        if start:
            sys.stdout.write('%s\r%s\r%s' % (colors[color], ' ' * 90, string))
        else:
            sys.stdout.write('%s%s' % (colors[color], string))
    return string


def inputos():
    return msvcrt.getch()


def input(last='', mask=string.ascii_letters + string.digits + string.punctuation + string.whitespace, color=9, hide=0):
    _mask_ = set()
    for every in mask:
        _mask_.add(ord(every))
    mask = _mask_
    string = ''
    print(last, True, color, False)
    last = last.split('\n')
    last = last[len(last) - 1]
    ch = 'q'
    while ord(ch) != 10:
        try:
            ch = msvcrt.getch()
        except OverflowError:
            ch = chr(1)
        if ord(ch) in mask:
            string += ch
        elif ord(ch) == 127:
            string = string[0:len(string) - 1]
        if hide == 0:
            print(last + string, False, color)
        elif hide == 1:
            print(last + '*' * len(string), False, color)
        elif hide == 2:
            print(last, False, color)
    return string


def updater(filename, path):
    ver = '%s_version' % filename
    last = 0
    try:
        version = open(ver, 'r+')
        vers = float(version.read())
    except:
        vers = 0
        last = 1
        print('ТЕКУЩАЯ ВЕРСИЯ НЕ УКАЗАНА/ФОРМАТ НЕ ВЕРЕН!!!!\nЗАГРУЗКА ПОСЛЕДНЕЙ ВЕРСИИ.....', color=0, clr=True)
    if vers != float(requests.get(path + '/' + ver).text):
        print('ВЕРСИЯ УСТАРЕЛА, ОБНОВЛЯЮ......', color=1, clr=True)
        new = open(filename, 'w+', encoding='utf-8')
        new.write(requests.get(path + '/' + filename).text)
        new.close()
        if last == 0:
            version.close()
        version = open(ver, 'w+')
        version.write(requests.get(path + '/' + ver).text)
        version.close()
        if sys.platform == 'win32':
            os.system('%s/%s' % (os.getcwd(), filename))
        else:
            os.system('python3 %s/%s' % (os.getcwd(), '123.py'))
    else:
        print('ИСПОЛЬЗУЕТСЯ АКТУАЛЬНАЯ ВЕРСИЯ', 1)

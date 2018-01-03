import os
import string
import sys
import base64
import json

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
head = requests.utils.default_headers()
head['User-Agent'] = 'HOTTABBE API'
version = 2
colors = ['\033[31m', '\033[32m', '\033[37m', '\033[34m', '\033[36m', '\033[33m', '\033[35m', '\033[30m', '\033[30m',
          '\033[39m']


# colors = Red,Green,White,Blue,Cyan,Yellow,Magenta,Grey,Black,Default

def clear():
    try:
        os.system('clear')
    except:
        os.system('cls')


def hot_api():
    return version


def readcfg(file_name):
    with open(file_name, encoding='utf-8') as code:
        try:
            code = json.load(code)
        except:
            input('Формат конфига не верен!!!!! \nЧтение невозможно\n')
    if code['version'] == '1.0':
        code_ = code['content']
        for i in range(16):
            code_ = base64.b64decode(code_).decode('utf-8')
        return json.loads(code_)


def writecfg(file_name, content):
    with open(file_name, 'r+', encoding='utf-8') as file:
        file_ = file.read()
        if len(file_) != 0:
            try:
                keys = json.loads(file_)
            except json.decoder.JSONDecodeError:
                keys = {}
            if 'content' in keys and 'version' in keys and keys['version'] == '1.0':
                keys_ = keys['content']
                for i in range(16):
                    keys_ = base64.b64decode(keys_)
                    keys_ = keys_.decode('utf-8')
                keys = json.loads(keys_)
                for every in content:
                    keys[every] = content[every]
            else:
                keys = content
        else:
            keys = content
        for i in range(16):
            keys = base64.b64encode(bytes(json.dumps(keys),'utf-8')).decode('utf-8')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json.dumps({'version': '1.0', 'content': keys}))



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
        sys.stdout.write('%s\n%s\x1b[0m' % (colors[color], string))
    else:
        if start:
            sys.stdout.write('%s\r%s\r%s\x1b[0m' % (colors[color], ' ' * 70, string))
        else:
            sys.stdout.write('%s%s\x1b[0m' % (colors[color], string))
    return string


def inputos():
    return msvcrt.getch()


def input(last='', mask=string.ascii_letters + string.digits + string.punctuation + string.whitespace, color=9, hide=0,
          null=False):
    if sys.platform != 'win32':
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
        if null == False and len(string) < 1:
            return '0'
        else:
            return string.split('\n')[0]
    else:
        while True:
            string = inputer(last)
            if not null:
                if len(string) > 0:
                    return string
                else:
                    print('Строка пустая,введите заново')
            else:
                return string


def updater(filename, path, params, launch='', rewrite=False):
    r = requests.post('%s/updater.php' % path, params)
    if rewrite:
        filename = launch
    if r.text != 'updated':
        print('ЗАГРУЗКА НОВОЙ ВЕРСИИ СКРИПТА......', color=1, clr=True)
        file = open(filename, 'w+', encoding='utf-8')
        file.write(r.text)
        file.close()
        if sys.platform == 'win32':
            os.system('%s/%s' % (os.getcwd(), launch))
        else:
            os.system('python3 %s/%s' % (os.getcwd(), launch))
    else:
        print('ИСПОЛЬЗУЕТСЯ АКТУАЛЬНАЯ ВЕРСИЯ', 1)


def formatter(values, length, delim):
    for i in range(len(values)):
        values[i] = str(values[i])
        if len(values[i]) < length[i]:
            values[i] = values[i] + ' ' * (length[i] - len(values[i]) - 1) + delim
        else:
            values[i] = values[i][0:length[i] - 1] + delim
    return values


def editcfg(file_name):
    lines = readcfg(file_name)
    string = ''
    print('Текущие значения ключей %s' % file_name, frame=True)
    f_lines = {}
    f_head = formatter(['Имя ключа', 'Значение', 'Комментарий'], [20, 25, 50], '┃')
    for every in f_head:
        string += every
    print(string + '\n' + '━' * 19 + '╋' + '━' * 24 + '╋' + '━' * 49 + '┫')
    for every in lines:
        string = ''
        f_lines[every] = formatter([every, lines[every]['value'], lines[every]['tip']], [20, 25, 50], '┃')
        for every in f_lines[every]:
            string += every
        print(string + '\n' + '━' * 19 + '╋' + '━' * 24 + '╋' + '━' * 49 + '┫')
    print('━' * 19 + '┻' + '━' * 24 + '┻' + '━' * 49 + '┛\n\n\n\n\n\n')
    print('Сейчас введите новые значения для ключей %s\nИли --- для того,чтобы оставить старое значение' % file_name)
    for every in lines:
        enter = input('Введите значение %s : ' % every, null=True)
        if enter != '---':
            lines[every] = enter
    writecfg(file_name, lines, tips=tips)
    print('Успешно перезаписано : %s !!!' % file_name, color=1)


def bugreport(vers, soft):
    print('Сейчас введите заголовок репорта,\nкоторый будет отражать всю суть ошибки.', frame=True)
    header = inputer('\n--> ')
    print('Кратко опишите возникающую проблему.', frame=True)
    error = inputer('\n--> ')
    print('Если известна строка, в которой возникает ошибка - напишите ее\n'
          'В противном случае - напишите "---".', frame=True)
    line = input('--> ', mask='1234567890-', color=4)
    print('Оцените ошибку\n'
          '1. Ошибка не важна\n'
          '2. Ошибка никак не нарушает работу скрипта\n'
          '3. Ошибка нарушает работу скрипта,но не крашит его\n'
          '4. Ошибка крашит скрипт,не давая совершить действия', color=4, frame=True)
    rate = input('--> ', color=4, mask='1234')
    data = {
        'head': header,
        'error': error,
        'line': line,
        'rate': rate,
        'version': vers,
        'soft': soft
    }
    print(requests.post('https://hottabbe.000webhostapp.com/reporter.php', data, headers=head).text, clr=True)

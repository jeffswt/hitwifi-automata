
import json
import tkinter
import sys
from tkinter import messagebox

import libhitwa


config_fn = 'config.json'

def main(argv):
    try:
        f = open('config.json', 'r', encoding='utf-8')
        s = f.read()
        s = '\n'.join(map(lambda x: x.split('#')[0], s.split('\n')))
        f.close()
        j = json.loads(s)
        username = j['username']
        password = j['password']
        locale = j['locale']
    except:
        f = open('config.json', 'w', encoding='utf-8')
        s = ('{\n'
             '    "username": "",  # Username / 用户名 / ユーザー名\n'
             '    "password": "",  # Password / 密码 / パスワード\n'
             '    "locale": "zh"  # Language: en / 简体中文: zh / 日本語: jp\n'
             '}')
        f.write(s)
        f.close()
        tk = tkinter.Tk()
        tk.withdraw()
        messagebox.showinfo('HITWiFi: Automata',
                            'The configuration file is missing or broken.\n'
                            'Edit config.json to update preferences.\n\n'
                            '配置文件丢失或已损坏。\n'
                            '用记事本编辑 config.json 更新用户名密码。\n\n'
                            '構成ファイルが欠落しているか壊れています。\n'
                            'config.jsonを編集して設定を更新します。')
        return
    print(username, password, locale)
    if len(argv) <= 1 or argv[1] != 'logout':
        result, message = libhitwa.do_login(username, password)
    else:
        result, message = libhitwa.do_logout()
    message = libhitwa.get_msg_lang(message, locale=locale)
    # draw message box
    tk = tkinter.Tk()
    tk.withdraw()
    if result:
        messagebox.showinfo('HITWiFi: Automata', message)
    else:
        messagebox.showerror('HITWiFi: Automata', message)
    return

if __name__ == '__main__':
    main(sys.argv)

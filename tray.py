
import wx
import wx.adv
import time
import socket
import platform
import subprocess
import threading
import json

import libhitwa


def get_ui_lang(msg, locale='en'):
    """ get_ui_lang(msg, locale='en'): Retrieve language string for codename
    @param msg <- str: the codename
    @param locale <- str: language to retrieve
    @return msg -> str: translated string """
    langs = {'en', 'zh', 'jp'}
    lang_list = {
        'General.Title': {
            'en': 'HITWiFi: Automata',
            'zh': 'HITWiFi: Automata',
            'jp': 'HITWiFi: Automata',
        },
        'MenuItem.NetStatus.UpdatePaused': {
            'en': '- Connectivity update paused',
            'zh': '- 网络连接检测已暂停',
            'jp': '- ネットワーク接続の更新が一時停止しました',
        },
        'MenuItem.NetStatus.Detecting': {
            'en': '- Detecting connectivity...',
            'zh': '- 正在检测网络连接...',
            'jp': '- ネットワーク接続の検出中...',
        },
        'MenuItem.NetStatus.NoNetwork': {
            'en': '× No network available',
            'zh': '× 无可用网络连接',
            'jp': '× 使えるネットワークがありません',
        },
        'MenuItem.NetStatus.WanConnected': {
            'en': '√ Connected to Internet (WAN)',
            'zh': '√ 已连接到互联网 (WAN)',
            'jp': 'o インタネット (WAN) に接続された',
        },
        'MenuItem.NetStatus.CanDisconnected': {
            'en': '× Campus Network disconnected',
            'zh': '× 校园网已断开',
            'jp': '× 学園ネットワークが切断された',
        },
        'MenuItem.NetStatus.CanConnected': {
            'en': '√ Connected to Campus Network',
            'zh': '√ 校园网已连接',
            'jp': 'o 学園ネットワークに接続された',
        },
        'MenuItem.DaemonStatus.Working': {
            'en': 'Pause autoconnect',
            'zh': '暂停自动连接',
            'jp': '自動接続を一時停止する',
        },
        'MenuItem.DaemonStatus.Paused': {
            'en': 'Resume autoconnect',
            'zh': '恢复自动连接',
            'jp': '自動接続を再開する',
        },
        'MenuItem.Login': {
            'en': 'Manually connect to network',
            'zh': '手动连接到校园网',
            'jp': '学園ネットワークに接続する',
        },
        'MenuItem.Logout': {
            'en': 'Disconnect from network',
            'zh': '断开校园网',
            'jp': '学園ネットワークから切断する',
        },
        'MenuItem.LoggingIn': {
            'en': 'Connecting to network...',
            'zh': '正在连接...',
            'jp': '接続しています...',
        },
        'MenuItem.LoggingOut': {
            'en': 'Logging out...',
            'zh': '正在登出...',
            'jp': '切断しています...',
        },
        'MenuItem.Settings': {
            'en': 'Settings',
            'zh': '设置',
            'jp': '設定',
        },
        'MenuItem.Exit': {
            'en': 'Exit',
            'zh': '退出',
            'jp': '終了',
        },
        'Notification.DaemonStatus.Pause': {
            'en': 'Paused automatic connection to the Campus Network.',
            'zh': '已暂停校园网自动连接。',
            'jp': '学園ネットワークへの自動接続を一時停止しました。',
        },
        'Notification.DaemonStatus.Resume': {
            'en': 'Resumed automatic connection to the Campus Network.',
            'zh': '已恢复校园网自动连接。',
            'jp': '学園ネットワークへの自動接続を再開しました。',
        },
        'Notification.DaemonStatus.TooManyFailures': {
            'en': 'Too many failed attempts, pausing automatic connection.',
            'zh': '连接失败次数过多，已暂停自动连接。',
            'jp': '失敗した試行が多すぎて、自動接続を一時停止します。',
        },
        'Settings.Title': {
            'en': 'Settings',
            'zh': '设置',
            'jp': '設定',
        },
        'Settings.Locale': {
            'en': 'Language',
            'zh': '语言',
            'jp': '言語',
        },
        'Settings.Username': {
            'en': 'Username',
            'zh': '用户名',
            'jp': 'ユーザー名',
        },
        'Settings.Password': {
            'en': 'Password',
            'zh': '密码',
            'jp': 'パスワード',
        },
        'Settings.OkButton': {
            'en': 'Save Changes',
            'zh': '保存设置',
            'jp': '設定を保存する',
        },
    }
    if msg not in lang_list:
        return msg
    if locale not in langs:
        locale = 'en'
    return lang_list[msg][locale]


def send_notification(title, message, *args, locale='en',
                      trans=(True, True), **kwargs):
    if trans[0]:
        title = get_ui_lang(title, locale=locale)
    if trans[1]:
        message = get_ui_lang(message, locale=locale)
    nm = wx.adv.NotificationMessage(title, message, *args, **kwargs)
    ic = wx.Icon('icon.png')
    # wx.adv.NotificationMessage.SetIcon(wx.Icon('icon.png'))
    nm.Show()
    return


class HwaConfigManager:
    def __init__(self):
        self.filename = 'config.json'
        self.default_data = {
            'locale': 'zh',
            'username': '',
            'password': '',
        }
        self.data = {}
        for i in self.default_data:
            self.data[i] = self.default_data[i]
        return

    def __contains__(self, x):
        return x in self.data

    def __getitem__(self, x):
        return self.data[x]

    def __setitem__(self, x, y):
        if x not in self.data:
            return
        self.data[x] = y
        return

    def load(self):
        try:
            fhandle = open(self.filename, 'r', encoding='utf-8')
            content = fhandle.read()
            fhandle.close()
            obj = json.loads(content)
            ndata = {}
            for i in self.default_data:
                ndata[i] = content[i]
            self.data = ndata
        except Exception:
            self.data = {}
            for i in self.default_data:
                self.data[i] = self.default_data[i]
            return False
        return True

    def save(self):
        try:
            content = json.dumps(self.data, indent=4)
            fhandle = open(self.filename, 'w', encoding='utf-8')
            fhandle.write(content)
            fhandle.close()
        except Exception:
            pass
        return
    pass


class HwaConfigFrame(wx.Frame):
    def __init__(self, config, *args, **kwargs):
        kwargs['style'] = (kwargs.get('style', 0) | wx.CAPTION |
                           wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.STAY_ON_TOP |
                           wx.SYSTEM_MENU)
        wx.Frame.__init__(self, *args, **kwargs)
        # data storage
        self.config = config
        self.lang_list = [
            ('en', 'English'),
            ('zh', '简体中文'),
            ('jp', '日本語'),
        ]
        # create data elements
        self.items = {}
        self.SetSize((361, 213))
        self.items['data-locale'] = wx.Choice(
            self, wx.ID_ANY, choices=list(i[1] for i in self.lang_list))
        # self.choice1.GetCurrentSelection()
        self.items['data-username'] = wx.TextCtrl(self, wx.ID_ANY, '')
        self.items['data-password'] = wx.TextCtrl(
            self, wx.ID_ANY, '', style=wx.TE_PASSWORD)
        self.items['button-ok'] = wx.Button(self, wx.ID_ANY, 'OK')
        # set properties
        self.SetTitle('Settings')
        self.SetIcon(wx.Icon('icon.png'))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(
                                 wx.SYS_COLOUR_3DFACE))
        self.items['data-locale'].SetSelection(
            dict((self.lang_list[i][0], i) for i in range(len(self.lang_list)))
            [self.config['locale']])
        self.items['button-ok'].SetMinSize((200, 26))
        # set layout
        self.items['vert-frame'] = wx.BoxSizer(wx.VERTICAL)
        self.items['input-grid'] = wx.FlexGridSizer(3, 2, 0, 0)
        self.items['text-locale'] = wx.StaticText(
            self, wx.ID_ANY, 'Locale')
        self.items['input-grid'].Add(self.items['text-locale'], 0, wx.ALL, 10)
        self.items['input-grid'].Add(
            self.items['data-locale'], 0, wx.ALL | wx.EXPAND, 5)
        self.items['text-username'] = wx.StaticText(
            self, wx.ID_ANY, 'Username')
        self.items['input-grid'].Add(
            self.items['text-username'], 0, wx.ALL, 10)
        self.items['input-grid'].Add(
            self.items['data-username'], 0, wx.ALL | wx.EXPAND, 5)
        self.items['text-password'] = wx.StaticText(
            self, wx.ID_ANY, 'Password')
        self.items['input-grid'].Add(
            self.items['text-password'], 0, wx.ALL, 10)
        self.items['input-grid'].Add(
            self.items['data-password'], 0, wx.ALL | wx.EXPAND, 5)
        self.items['input-grid'].AddGrowableCol(1)
        self.items['vert-frame'].Add(
            self.items['input-grid'], 1, wx.EXPAND | wx.LEFT |
            wx.RIGHT | wx.TOP, 16)
        self.items['vert-frame'].Add((0, 0), 0, 0, 0)
        self.items['vert-frame'].Add(
            self.items['button-ok'], 0, wx.ALIGN_CENTER | wx.ALL, 12)
        self.SetSizer(self.items['vert-frame'])
        self.update_text()
        # bind events
        self.Bind(wx.EVT_CHOICE, self.eventh_choice, self.items['data-locale'])
        self.Bind(wx.EVT_BUTTON, self.eventh_ok, self.items['button-ok'])
        self.Bind(wx.EVT_CLOSE, self.eventh_close, self)
        self.Layout()
        return

    def update_text(self):
        locale = self.config['locale']
        self.SetTitle(get_ui_lang('Settings.Title', locale=locale))
        self.items['text-locale'].SetLabelText(get_ui_lang(
            'Settings.Locale', locale=locale))
        self.items['text-username'].SetLabelText(get_ui_lang(
            'Settings.Username', locale=locale))
        self.items['text-password'].SetLabelText(get_ui_lang(
            'Settings.Password', locale=locale))
        self.items['button-ok'].SetLabelText(get_ui_lang(
            'Settings.OkButton', locale=locale))
        self.Layout()
        return

    def eventh_choice(self, event):
        self.config['locale'] = self.lang_list[
            self.items['data-locale'].GetCurrentSelection()][0]
        self.update_text()
        return

    def eventh_ok(self, event):
        self.Close()
        return
    
    def eventh_close(self, event):
        self.config['username'] = self.items['data-username'].GetLineText(0)
        self.config['password'] = self.items['data-password'].GetLineText(0)
        print(self.config.data)
        event.Skip()
        return
    pass


def update_config_gui(config):
    frame = HwaConfigFrame(config, None, wx.ID_ANY, '')
    frame.Show()
    return


class HwaTrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, config_mgr):
        wx.adv.TaskBarIcon.__init__(self)
        # Get menu item IDs
        # Why use ID? because menu items change.
        # And I don't like to bind things frequently.
        self.item_ids = {
            'net-status': wx.NewIdRef(),
            'daemon-status': wx.NewIdRef(),
            'login': wx.NewIdRef(),
            'logout': wx.NewIdRef(),
            'connect-status': wx.NewIdRef(),
            'settings': wx.NewIdRef(),
            'exit': wx.NewIdRef(),
        }
        self.states = {
            'net-status': 'detecting',
            'daemon-working': False,
            'daemon-thread': None,
            'terminate-all': False,
            'logging-in': False,
            'logging-out': False,
            'login-failed-attempts': 0,
        }
        self.config = config_mgr
        # Bind icon and title
        self.SetIcon(wx.Icon('icon.png'),
                     get_ui_lang('General.Title',
                     locale=self.config['locale']))
        # Bind Entries
        self.Bind(wx.EVT_MENU, self.eventh_net_status,
                  id=self.item_ids['net-status'])
        self.Bind(wx.EVT_MENU, self.eventh_daemon_status,
                  id=self.item_ids['daemon-status'])
        self.Bind(wx.EVT_MENU, self.eventh_login,
                  id=self.item_ids['login'])
        self.Bind(wx.EVT_MENU, self.eventh_logout,
                  id=self.item_ids['logout'])
        self.Bind(wx.EVT_MENU, self.eventh_connect_status,
                  id=self.item_ids['connect-status'])
        self.Bind(wx.EVT_MENU, self.eventh_settings,
                  id=self.item_ids['settings'])
        self.Bind(wx.EVT_MENU, self.eventh_exit,
                  id=self.item_ids['exit'])
        # Start daemon
        self.states['daemon-working'] = True
        self.start_daemon()
        return

    def eventh_net_status(self, event):
        return

    def eventh_daemon_status(self, event):
        if self.states['daemon-working']:
            send_notification('General.Title',
                              'Notification.DaemonStatus.Pause',
                              locale=self.config['locale'],
                              flags=wx.ICON_INFORMATION)
            self.states['daemon-working'] = False
            self.states['net-status'] = 'paused'
        else:
            send_notification('General.Title',
                              'Notification.DaemonStatus.Resume',
                              locale=self.config['locale'],
                              flags=wx.ICON_INFORMATION)
            self.states['daemon-working'] = True
            self.states['net-status'] = 'detecting'
        return

    def eventh_login(self, event):
        if self.states['logging-in'] or self.states['logging-out']:
            return
        if self.states['net-status'] != 'can-disconnected':
            return
        self.states['logging-in'] = True
        status, message = libhitwa.net_login(
            self.config['username'],
            self.config['password'])
        message = libhitwa.get_msg_lang(message, locale=self.config['locale'])
        if status:
            send_notification('General.Title', message,
                              trans=(True, False),
                              locale=self.config['locale'],
                              flags=wx.ICON_INFORMATION)
            self.states['net-status'] = 'can-connected'
            self.states['login-failed-attempts'] = 0
        else:
            send_notification('General.Title', message,
                              trans=(True, False),
                              locale=self.config['locale'],
                              flags=wx.ICON_EXCLAMATION)
            self.states['login-failed-attempts'] += 1
        self.states['logging-in'] = False
        return

    def eventh_logout(self, event):
        if self.states['logging-out'] or self.states['logging-in']:
            return
        if self.states['net-status'] != 'can-connected':
            return
        self.states['logging-out'] = True
        self.states['daemon-working'] = False
        self.states['net-status'] = 'paused'
        status, message = libhitwa.net_logout()
        message = libhitwa.get_msg_lang(message, locale=self.config['locale'])
        if status:
            send_notification('General.Title', message,
                              trans=(True, False),
                              locale=self.config['locale'],
                              flags=wx.ICON_INFORMATION)
        else:
            send_notification('General.Title', message,
                              trans=(True, False),
                              locale=self.config['locale'],
                              flags=wx.ICON_EXCLAMATION)
        self.states['logging-out'] = False
        return

    def eventh_connect_status(self, event):
        return

    def eventh_settings(self, event):
        return

    def eventh_exit(self, event):
        self.states['terminate-all'] = True
        self.RemoveIcon()
        self.states['daemon-thread'].join()
        wx.Exit()
        return

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.item_ids['net-status'], get_ui_lang(
                    {'paused': 'MenuItem.NetStatus.UpdatePaused',
                     'detecting': 'MenuItem.NetStatus.Detecting',
                     'no-network': 'MenuItem.NetStatus.NoNetwork',
                     'wan-connected': 'MenuItem.NetStatus.WanConnected',
                     'can-disconnected': 'MenuItem.NetStatus.CanDisconnected',
                     'can-connected': 'MenuItem.NetStatus.CanConnected'}
                    [self.states['net-status']],
                    locale=self.config['locale']))
        menu.AppendSeparator()
        menu.Append(self.item_ids['daemon-status'], get_ui_lang(
                    'MenuItem.DaemonStatus.Working' if
                    self.states['daemon-working'] else
                    'MenuItem.DaemonStatus.Paused',
                    locale=self.config['locale']))
        if self.states['logging-in'] or self.states['logging-out']:
            menu.Append(self.item_ids['connect-status'], get_ui_lang(
                        'MenuItem.LoggingIn' if
                        self.states['logging-in'] else
                        'MenuItem.LoggingOut',
                        locale=self.config['locale']))
        else:
            if self.states['net-status'] == 'can-disconnected':
                menu.Append(self.item_ids['login'], get_ui_lang(
                            'MenuItem.Login',
                            locale=self.config['locale']))
            if self.states['net-status'] == 'can-connected':
                menu.Append(self.item_ids['logout'], get_ui_lang(
                            'MenuItem.Logout',
                            locale=self.config['locale']))
        menu.Append(self.item_ids['settings'], get_ui_lang(
                    'MenuItem.Settings',
                    locale=self.config['locale']))
        menu.Append(self.item_ids['exit'], get_ui_lang(
                    'MenuItem.Exit',
                    locale=self.config['locale']))
        return menu

    def start_daemon(self):
        def daemon(self):
            timestamp = time.time()
            delay = 3
            connect_cooldown = 10
            worker = libhitwa.NetworkConnectivityBuffer()
            while True:
                # if program stopped
                if self.states['terminate-all']:
                    break
                # if daemon paused
                if not self.states['daemon-working']:
                    self.states['net-status'] = 'paused'
                    time.sleep(delay)
                    timestamp = time.time()
                    continue
                # update network status
                worker.update_status()
                self.states['net-status'] = worker.get_status()
                # attempt connection
                if (not self.states['logging-in'] and not
                        self.states['logging-out'] and
                        self.states['net-status'] == 'can-disconnected'):
                    self.states['logging-in'] = True
                    status, message = libhitwa.net_login(
                        self.config['username'],
                        self.config['password'])
                    if status:
                        # successfully connected
                        message = libhitwa.get_msg_lang(
                                message, locale=self.config['locale'])
                        send_notification('General.Title', message,
                                          trans=(True, False),
                                          locale=self.config['locale'],
                                          flags=wx.ICON_INFORMATION)
                        self.states['net-status'] = 'can-connected'
                        self.states['login-failed-attempts'] = 0
                        self.states['logging-in'] = False
                    else:
                        # connection failed
                        self.states['login-failed-attempts'] += 1
                        if self.states['login-failed-attempts'] >= 3:
                            # too many failures, pausing daemon
                            send_notification(
                                'General.Title',
                                'Notification.DaemonStatus.TooManyFailures',
                                locale=self.config['locale'],
                                flags=wx.ICON_EXCLAMATION)
                            self.states['net-status'] = 'paused'
                            self.states['daemon-working'] = False
                        self.states['logging-in'] = False
                    time.sleep(connect_cooldown)
                # sleep and update timestamp
                ntimestamp = time.time()
                time.sleep(max(0.5, delay - (ntimestamp - timestamp)))
                timestamp = ntimestamp
            return
        th = threading.Thread(target=daemon, args=[self])
        th.start()
        self.states['daemon-thread'] = th
        return
    pass


class HwaTrayIconApp(wx.App):
    def OnInit(self):
        HwaTrayIcon({'locale': 'zh', 'username': '---', 'password': '---'})
        return True


if __name__ == "__main__":
    app = HwaTrayIconApp()
    app.MainLoop()

# MIT License
#
# Copyright (c) 2019 Geoffrey Tang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import cryptography.hazmat.primitives.ciphers
import cryptography.hazmat.backends
import json
import os
import platform
import requests
import re
import socket
import subprocess
import urllib

__all__ = [
    'get_msg_lang',
    'transcript_data',
    'net_login',
    'net_logout',
    'NetworkConnectivityBuffer',
]


def get_msg_lang(msg, locale='en'):
    """ get_msg_lang(msg, locale='en'): Retrieve language string for codename
    @param msg <- str: the codename
    @param locale <- str: language to retrieve
    @return msg -> str: translated string """
    langs = {'en', 'zh', 'jp'}
    lang_list = {
        'ALREADY_ONLINE': {
            'en': 'The device is already connected to the Internet.',
            'zh': '设备已连接到互联网。',
            'jp': 'このデバイスはすでにインターネットに接続されています。',
        },
        'ALREADY_OFFLINE': {
            'en': 'The device is already disconnected.',
            'zh': '用户已登出校园网。',
            'jp': 'このデバイスはすでにインターネットから切断されています。',
        },
        'NO_NETWORK': {
            'en': 'The device is not properly connected to HIT campus '
                  'network (or any).',
            'zh': '用户不处于校园网环境中。',
            'jp': 'このデバイスがキャンパスネットワークに適切に接続'
                  'されていません。',
        },
        'MISSING_EPORTAL': {
            'en': 'Cannot locate the ePortal address.',
            'zh': '无法获取认证服务器地址。',
            'jp': 'イーポータルアドレスが見つかりません。',
        },
        'NO_REPONSE': {  # No Response (
            'en': 'ePortal server did not response.',
            'zh': '认证服务器未应答。',
            'jp': '認証サーバーが応答しませんでした。',
        },
        'EMPTY_USERNAME': {
            'en': 'Username should not be empty.',
            'zh': '用户名不得为空。',
            'jp': 'ユーザー名は空にしないでください。',
        },
        'EMPTY_PASSWORD': {
            'en': 'Password should not be empty.',
            'zh': '密码不得为空。',
            'jp': 'パスワードは空にしないでください。',
        },
        'INCORRECT_USERNAME': {
            'en': 'The user does not exist.',
            'zh': '用户名不存在。',
            'jp': 'ユーザーが存在しません。',
        },
        'INCORRECT_PASSWORD': {
            'en': 'The password is incorrect.',
            'zh': '密码输入错误。',
            'jp': 'パスワードが間違っています。',
        },
        'LOGIN_SUCCESS': {
            'en': 'Successfully connected to HIT campus network!',
            'zh': '成功连接到校园网！',
            'jp': 'ログインに成功しました！',
        },
        'LOGOUT_SUCCESS': {
            'en': 'Successfully disconnected!',
            'zh': '已登出校园网。',
            'jp': 'ログアウトしました！',
        },
        'LOGOUT_FAILED': {
            'en': 'Failed to logout (what the ****)',
            'zh': '登出失败 (smg)',
            'jp': 'ログアウトに失敗しました (なに)',
        },
    }
    if msg not in lang_list:
        return msg
    if locale not in langs:
        locale = 'en'
    return lang_list[msg][locale]


def parse_url(url):
    """ parse_url(url): Parse URL according to urllib.parse
    @param url <- str: the URL string
    @return components -> dict(str: *): the URL components """
    _1, _2, _3, _4, _5, _6 = urllib.parse.urlparse(url)
    _5 = urllib.parse.parse_qs(_5, keep_blank_values=True)
    return {
        'scheme': _1,
        'netloc': _2,
        'path': _3,
        'params': _4,
        'query': _5,
        'fragment': _6,
    }


def join_query(queries):
    """ join_query(queries): Join urllib queries
    @param queries <- dict(str: list(str)): queries parsed by
           urllib.parse.parse_qs
    @return qs -> str: the query string """
    return '&'.join('&'.join(urllib.parse.quote(i) + '=' +
                             urllib.parse.quote(j) for j in queries[i])
                    for i in queries)


def ping(host, timeout=1.0):
    """ ping(host, timeout): Ping given host and return if accessible
    @param host <- str: hostname
    @param time <- float: timeout in seconds """
    if platform.system().lower() == 'windows':
        params = ['ping.exe', host, '-n', '1',
                  '-w', str(int(timeout * 1000))]
    else:
        params = ['ping', host, '-c', '1',
                  '-w', str(timeout)]
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen(
        args=params,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=si
    )
    try:
        ret = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        return False
    return ret == 0


def transcript_data(data, encrypt=True):
    if encrypt:
        backend = cryptography.hazmat.backends.default_backend()
        key = os.urandom(32)  # key
        iv = os.urandom(16)  # initialization vector
        # Generate encrypted message
        cipher = cryptography.hazmat.primitives.ciphers.Cipher(
            cryptography.hazmat.primitives.ciphers.algorithms.AES(key),
            cryptography.hazmat.primitives.ciphers.modes.CBC(iv),
            backend=backend)
        encryptor = cipher.encryptor()
        data = data.encode('utf-8')
        padded_data = data + b'\x00' * (len(data) // 16 * 16 + 16 - len(data))
        message = encryptor.update(padded_data) + encryptor.finalize()
        # pack into data
        blob = key + iv + (str(len(data)) + ';').encode('utf-8') + message
        return base64.b64encode(blob).decode('utf-8')
    else:
        blob = base64.b64decode(data.encode('utf-8'))
        # unpack values
        key = blob[:32]
        blob = blob[32:]
        iv = blob[:16]
        blob = blob[16:]
        dsize = blob.split(b';')[0]
        message = blob[(len(dsize) + 1):]
        # retrieve message
        backend = cryptography.hazmat.backends.default_backend()
        cipher = cryptography.hazmat.primitives.ciphers.Cipher(
            cryptography.hazmat.primitives.ciphers.algorithms.AES(key),
            cryptography.hazmat.primitives.ciphers.modes.CBC(iv),
            backend=backend)
        decryptor = cipher.decryptor()
        text = decryptor.update(message) + decryptor.finalize()
        return text[:int(dsize.decode('utf-8'))].decode('utf-8')
    return


def net_login(username, password):
    """ net_login(username, password): Login to HIT campus network
    @param username <- str: the 10-digit username you would enter
    @param password <- str: the password you specified
    @return status -> bool: True if connected to network
    @return message -> str: describes the reason related to status """
    urls = {
        'redirect': 'http://www.msftconnecttest.com/redirect',
        'auth-ip': '202.118.253.94:8080',
        'auth-domain': 'http://202.118.253.94:8080',
        'auth-index': '/eportal/index.jsp',
        'auth-login': '/eportal/InterFace.do?method=login'
    }
    # retrieve access point names
    try:
        req = requests.get(urls['redirect'])
        req.encoding = 'utf-8'
    except Exception as err:
        return False, 'NO_NETWORK'
    if 'https://go.microsoft.com/fwlink/' in req.text:
        return True, 'ALREADY_ONLINE'
    probable_urls = re.findall(r'[\'\"]([^\'\"]*?)[\'\"]', req.text)
    eportal_url = list(filter(lambda x: x.startswith(urls['auth-domain'] +
                                                     urls['auth-index']),
                              probable_urls))
    if len(eportal_url) == 0:
        return False, 'MISSING_EPORTAL'
    eportal_url = eportal_url[0]
    # generate login query
    post_query = {
        'userId': [username],
        'password': [password],
        'service': [''],
        'queryString': [urllib.parse.quote(join_query(parse_url(
                        eportal_url)['query']))],
        'operatorPwd': [''],
        'operatorUserId': [''],
        'validcode': [''],
        'passwordEncrypt': ['false'],
    }
    post_string = join_query(post_query)
    headers = {
        'Host': urls['auth-ip'],
        'Origin': urls['auth-domain'],
        'Referer': eportal_url,
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                       'Chrome/75.0.3770.142 Safari/537.36'),
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': str(len(post_string)),
    }
    try:
        req = requests.post(urls['auth-domain'] + urls['auth-login'],
                            data=post_string,
                            headers=headers)
        req.encoding = 'utf-8'
    except Exception as err:
        return False, 'NO_NETWORK'
    if type(req.text) != dict:
        try:
            result = json.loads(req.text)
        except Exception as err:
            return False, 'NO_REPONSE'
    else:
        result = req.text
    if result.get('result', 'fail') != 'success':
        msg = result.get('message', '')
        info_map = {
            ('用户名不能为空', 'EMPTY_USERNAME'),
            ('用户不存在', 'INCORRECT_USERNAME'),
            ('用户密码错误', 'INCORRECT_PASSWORD'),
            ('密码不能为空', 'EMPTY_PASSWORD'),
        }
        for _ in info_map:
            if msg.startswith(_[0]):
                return False, _[1]
        return False, msg
    return True, 'LOGIN_SUCCESS'


def net_logout():
    """ net_logout(): Logout from HIT campus network
    @return status -> bool: True if disconnected from Internet
    @return message -> str: describes the reason related to status """
    urls = {
        'auth-ip': '202.118.253.94:8080',
        'auth-domain': 'http://202.118.253.94:8080',
        'auth-login': '/eportal/InterFace.do?method=logout'
    }
    payload = ''
    headers = {
        'Host': urls['auth-ip'],
        'Origin': urls['auth-domain'],
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                       'Chrome/75.0.3770.142 Safari/537.36'),
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': str(len(payload)),
    }
    try:
        req = requests.post(urls['auth-domain'] + urls['auth-login'],
                            data=payload,
                            headers=headers)
        req.encoding = 'utf-8'
    except Exception as err:
        return True, 'NO_NETWORK'
    if type(req.text) != dict:
        try:
            result = json.loads(req.text)
        except Exception as err:
            return False, 'NO_REPONSE'
    else:
        result = req.text
    if (result.get('result', '') == 'fail' and
            result.get('message', '') == '用户已不在线'):
        return True, 'ALREADY_OFFLINE'
    if result.get('result', 'fail') != 'success':
        return False, result.get('message', 'LOGOUT_FAILED')
    return True, 'LOGOUT_SUCCESS'


class NetworkConnectivityBuffer:
    def __init__(self):
        self.buffers = []
        self.buffer_size = 3
        return

    def check_connectivity(self, timeout=1.0):
        www_addr = ('www.baidu.com', 80)
        cnet_addr = ('202.118.253.94', 8080)
        result = {
            'any-network': False,
            'campus-network': False,
            'internet': False,
        }
        # determine if a network is connected
        try:
            socket.create_connection(www_addr, timeout=timeout)
            result['any-network'] = True
        except OSError:
            return result
        # check if is under campus network
        try:
            socket.create_connection(cnet_addr, timeout=timeout)
            result['campus-network'] = True
        except OSError:
            pass
        # check if is connected to internet
        if ping(www_addr[0], timeout=timeout):
            result['internet'] = True
        return result

    def update_status(self):
        res = self.check_connectivity(timeout=0.5)
        res_hash = '%d,%d,%d' % (res['any-network'], res['campus-network'],
                                 res['internet'])
        res_map = {
            '1,0,1': 'wan-connected',  # Wide Area Network
            '1,1,0': 'can-disconnected',  # Campus Area Network
            '1,1,1': 'can-connected',
        }
        res = res_map.get(res_hash, 'no-network')
        self.buffers.append(res)
        if len(self.buffers) > self.buffer_size:
            self.buffers.pop(0)
        return

    def get_status(self):
        if len(self.buffers) < self.buffer_size:
            return 'detecting'
        res = 0
        ranking = {
            'paused': -2,
            'detecting': -1,
            'no-network': 0,
            'wan-connected': 1,
            'can-disconnected': 2,
            'can-connected': 3,
        }
        inv_ranking = dict((ranking[i], i) for i in ranking)
        for stat in self.buffers:
            res = max(res, ranking[stat])
        return inv_ranking[res]

    def clear_status(self):
        self.buffers = []
        return
    pass

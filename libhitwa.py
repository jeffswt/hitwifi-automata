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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = [
    'get_msg_lang',
    'do_login',
    'do_logout',
]

import json
import requests
import re
import urllib


def get_msg_lang(msg, locale='en'):
    langs = {'en', 'zh', 'jp'}
    lang_list = {
        'ALREADY_ONLINE': {
            'en': 'The device is already connected to the Internet.',
            'zh': '人家早就已经连上网了喵   ԅ(¯﹃¯ԅ)',
            'jp': 'このデバイスはすでにインターネットに接続されています。',
        },
        'ALREADY_OFFLINE': {
            'en': 'The device is already disconnected.',
            'zh': '人家早就断网了喵   (ง •_•)ง',
            'jp': 'このデバイスはすでにインターネットから切断されています。',
        },
        'NO_NETWORK': {
            'en': 'The device is not properly connected to HIT campus '
                  'network (or any).',
            'zh': '人家根本就没有连上校园网的喵   ~(￣▽￣)~*',
            'jp': 'このデバイスがキャンパスネットワークに適切に接続'
                  'されていません。',
        },
        'MISSING_EPORTAL': {
            'en': 'Cannot locate the ePortal address.',
            'zh': '人家不知道怎么登录校园网的喵   ≧ ﹏ ≦',
            'jp': 'イーポータルアドレスが見つかりません。',
        },
        'NO_REPONSE': {  # No Response (
            'en': 'ePortal server did not response.',
            'zh': '服务器菌不回复人家的喵   o(TヘTo)',
            'jp': '認証サーバーが応答しませんでした。',
        },
        'EMPTY_USERNAME': {
            'en': 'Username should not be empty.',
            'zh': '好好把用户名给人家填上啊喵   (ノ｀Д)ノ',
            'jp': 'ユーザー名は空にしないでください。',
        },
        'EMPTY_PASSWORD': {
            'en': 'Password should not be empty.',
            'zh': '好好把密码给人家填上啊喵   (σ｀д′)σ',
            'jp': 'パスワードは空にしないでください。',
        },
        'INCORRECT_USERNAME': {
            'en': 'The user does not exist.',
            'zh': '这个用户根本根本就没有的喵   (lll￢ω￢)',
            'jp': 'ユーザーが存在しません。',
        },
        'INCORRECT_PASSWORD': {
            'en': 'The password is incorrect.',
            'zh': '密码敲错了啊的喵   (⊙o⊙)？',
            'jp': 'パスワードが間違っています。',
        },
        'LOGIN_SUCCESS': {
            'en': 'Successfully connected to HIT campus network!',
            'zh': '连上网了喵!   d=====(￣▽￣*)b',
            'jp': 'ログインに成功しました！',
        },
        'LOGOUT_SUCCESS': {
            'en': 'Successfully disconnected!',
            'zh': '网咋就断了喵   (。_。)',
            'jp': 'ログアウトしました！',
        },
        'LOGOUT_FAILED': {
            'en': 'Failed to logout (what the ****)',
            'zh': '没断开网 (smg)',
            'jp': 'ログアウトに失敗しました (なに)',
        },
    }
    if msg not in lang_list:
        return msg
    if locale not in langs:
        locale = 'en'
    return lang_list[msg][locale]


def parse_url(url):
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
    return '&'.join('&'.join(urllib.parse.quote(i) + '=' +
                             urllib.parse.quote(j) for j in queries[i])
                    for i in queries)


def do_login(username, password):
    """ do_login(username, password): Login to HIT campus network
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


def do_logout():
    """ do_logout(): Logout from HIT campus network
    @return status -> bool: True if logged out from campus network
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
        return False, 'NO_NETWORK'
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

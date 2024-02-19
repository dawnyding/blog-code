#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/28 11:01 
# @Author : dawny 
# @desc : 登录、获取session

import requests
from dingtalkchatbot.chatbot import DingtalkChatbot
import random
from hashlib import md5
import json


class MyZentao:
    def __init__(self, config):
        self._config = config
        self._loginurl = config.get_host() + "/zentao/user-login.html"
        self._session = requests.session()

        # 钉钉机器人
        webhook = config.get_webhook()
        secret = config.get_secret()
        self._robot = DingtalkChatbot(webhook, secret=secret)

    # pwd加密计算
    def computePasswordStrength(self, pwd):
        if len(pwd) == 0:
            return 0

        h = 0
        e = len(pwd)
        c = ""
        a = [0] * 3
        for i in pwd:
            letter = ord(str(i))
            if letter >= 48 and letter <= 57:
                a[2] = 2
            elif letter >= 65 and letter <= 90:
                a[1] = 2
            elif letter >= 97 and letter <= 122:
                a[0] = 1
            else:
                a[3] = 3
            if c != i:
                c += i
        if len(c) > 4:
            h += len(c) - 4
        g = f = 0
        for i in a:
            f += 1
            g += i
        h += g + (2 * (f - 2))
        if e < 6 and h >= 10:
            h = 9
        h = min(h, 29)
        h = h // 10
        return h

    def get_rank(self):
        url = self._config.get_host() + "/zentao/user-refreshRandom.html"
        res = self._session.get(url)
        res = res.text
        return res

    def login(self):
        password = str(self._config.get_password())
        rank = str(self.get_rank())

        body = {
            "account": self._config.get_account(),
            "password": md5((md5(password.encode('utf8')).hexdigest() + rank).encode('utf8')).hexdigest(),
            "passwordStrength": self.computePasswordStrength(password),
            "referer": "/zentao/",
            "verifyRand": rank,
            "keepLogin": 1,
            "captcha": ""
        }
        body_str = json.dumps(body)
        print(body_str)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }

        response = self._session.post(self._loginurl, headers=headers, data=body)

        with response:
            content = response.text
            if "self.location=" in content:
                print(" login success")
                return True
            elif "登录失败，请检查您的用户名或密码是否填写正确" in content:
                print("登录失败，请检查您的用户名或密码是否填写正确")
                return False
            else:
                print("login fail")
                return False

    def send_markdown(self, title, text):
        self._robot.send_markdown(title, text, is_at_all=True)

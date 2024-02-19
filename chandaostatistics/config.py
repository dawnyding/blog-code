#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/28 10:53 
# @Author : dawny 
# @desc : 读取配置文件

import json
import os


class Config:
    def __init__(self):
        config_path = "config.json"
        if not os.path.exists(config_path):
            print("config.json文件不存在")
        else:
            with open(config_path, 'r') as configFile:
                table = json.load(configFile)
                self._host = table["host"]
                self._account = table["account"]
                self._pwd = table["password"]
                self._webhook = table["webhook"]
                self._secret = table["secret"]
                self._pagepath = table["page_path"]

    def get_host(self):
        return self._host

    def get_account(self):
        print(f"account:{self._account}")
        return self._account

    def get_password(self):
        print(f"pwd:{self._pwd}")
        return self._pwd

    def get_webhook(self):
        return self._webhook

    def get_secret(self):
        return self._secret

    def get_pagepath(self):
        return self._pagepath

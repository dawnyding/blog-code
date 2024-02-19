#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/28 13:45 
# @Author : Renyjenny 
# @desc : 爬虫

import my_zentao
from lxml import etree
import datetime


class MyTask(my_zentao.MyZentao):
    def request(self):
        url = self._config.get_host() + self._config.get_pagepath()

        success = self.login()
        if success:
            response = self._session.get(url)
            with response:
                content = response.text
                html = etree.HTML(content)

                tasks = html.xpath("//table[@id='bugList']//tbody/tr")
                count = todo_num = 0
                bug_list = []

                for i,task in enumerate(tasks):
                    # 任务id
                    id = task.xpath("./@data-id")
                    id_str = str(id[0])
                    count += 1

                    # 状态
                    status = task.xpath("./td[contains(@class, 'c-status')]/@title")
                    if status[0] != '激活':
                        continue
                    todo_num += 1

                    # 组合bug list
                    content = task.xpath("./td[@class='c-title text-left']/@title")
                    content_str = str(content[0])

                    assigned_to = task.xpath("./td[contains(@class, 'c-assignedTo')]//text()")
                    assigned_to_str = str(assigned_to[1])

                    bug_list_item = "{0} {1}===>{2}".format(id_str, content_str, assigned_to_str)
                    bug_list.append(bug_list_item)

                # 组合markdown格式
                msg = "### [截止{}，共有{}个bug未解决，{}个bug待回归。](禅道地址)".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), todo_num, count - todo_num)
                msg = msg + "\n\n* * *\n"
                for i in bug_list:
                    msg = msg + '\n- ' + str(i)

                print(msg)
                # self.send_markdown("禅道提醒", msg)



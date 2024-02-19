#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/28 11:18 
# @Author : dawny 
# @desc : 启动类
import config,my_task


if __name__ == '__main__':

    config = config.Config()
    task = my_task.MyTask(config)
    task.request()
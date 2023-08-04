# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: plugin-framework
# author: "Lei Yong"
# creation time: 2023/8/4 5:13 PM
# Email: leiyong711@163.com

from utils.log import lg
from utils.AbstractPlugin import AbstractPlugin


class Plugin(AbstractPlugin):

    SLUG = "gpt"    # 插件唯一标识符
    PRIORITY = 0    # 插件优先级

    def handle(self, text, parsed):
        """处理函数"""
        lg.info(f"当前处理插件为 gpt 插件")
        self.plugin_manager.debug("gpt插件")

    def isValid(self, text, parsed):
        return 'gpt' in text.lower()

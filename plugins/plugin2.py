# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: plugin-framework
# author: "Lei Yong"
# creation time: 2023/8/4 5:13 PM
# Email: leiyong711@163.com

from utils.log import lg
from utils.AbstractPlugin import AbstractPlugin, PluginCannotProcessError


class Plugin(AbstractPlugin):

    SLUG = "echo"   # 插件唯一标识符
    ALIAS = "插件2"  # 插件别名
    PRIORITY = 1    # 插件优先级

    def handle(self, text, parsed):
        """处理函数"""
        lg.info(f"当前处理插件为 echo 插件")
        self.plugin_manager.debug("echo插件")
        raise PluginCannotProcessError(f"{self.SLUG}插件无法处理该事件")

    def isValid(self, text, parsed):
        return '传话' in text

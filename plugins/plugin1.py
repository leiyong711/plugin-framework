# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: plugin-framework
# author: "Lei Yong"
# creation time: 2023/8/4 5:13 PM
# Email: leiyong711@163.com

from utils.log import lg
from utils.AbstractPlugin import AbstractPlugin, PluginCannotProcessError


class Plugin(AbstractPlugin):

    SLUG = "poem"   # 插件唯一标识符
    ALIAS = "插件1"  # 插件别名
    PRIORITY = 0    # 插件优先级

    def handle(self, text, parsed):
        """处理函数"""
        lg.info(f"当前处理插件为 poem 插件")
        self.plugin_manager.debug("poem插件")
        raise PluginCannotProcessError(f"{self.SLUG}插件无法处理该事件")

    def isValid(self, text, parsed):
        return "写" in text and "诗" in text

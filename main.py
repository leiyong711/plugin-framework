# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: plugin-framework
# author: "Lei Yong"
# creation time: 2023/8/4 5:19 PM
# Email: leiyong711@163.com

from utils.log import lg
from utils.plugin_loader import get_plugins
from utils.AbstractPlugin import AbstractPlugin


class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        if isinstance(plugin, AbstractPlugin):
            self.plugins.append(plugin)
        else:
            raise ValueError("插件必须继承自AbstractPlugin")

    def load_plugins_from_folder(self):
        self.plugins = get_plugins(self)

    def run_plugins(self, text, parsed):
        for plugin in self.plugins:
            if plugin.isValid(text, parsed):
                plugin.handle(text, parsed)
                return
        lg.info("没有匹配的技能")

    def debug(self, msg):
        """调试方法"""
        lg.debug(f"我是插件管理器的debug方法，我被 {msg} 调用了")


if __name__ == '__main__':
    # 创建 PluginManager 实例
    plugin_manager = PluginManager()
    # 从指定文件夹加载插件
    plugin_manager.load_plugins_from_folder()

    while True:
        text = input("请输入文本：")
        lg.info(f"输入文本为：{text}")
        # 运行插件
        plugin_manager.run_plugins(text, "parsed")


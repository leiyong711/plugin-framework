# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: plugin-framework
# author: "Lei Yong"
# creation time: 2023/8/4 5:18 PM
# Email: leiyong711@163.com

import pkgutil
from utils.config import Config
from utils import constants
from utils.log import lg
from utils.AbstractPlugin import AbstractPlugin


_has_init = False

# 查询在运行的插件
_plugins_query = []
config = Config()


def init_plugins(con):
    """
    动态加载技能插件

    参数：
    con -- 会话模块
    """

    global _has_init
    locations = [constants.PLUGIN_PATH, constants.CONTRIB_PATH, constants.CUSTOM_PATH]
    lg.debug(f"检查插件目录：{locations}")

    global _plugins_query
    nameSet = set()

    for finder, name, ispkg in pkgutil.walk_packages(locations):

        # 重新加载模块
        try:
            importlib.reload(mod)
        except ModuleNotFoundError:
            ...
        except UnboundLocalError:
            ...

        try:
            loader = finder.find_module(name)
            mod = loader.load_module(name)
        except Exception:
            lg.warning(f"插件 {name} 加载出错，跳过", exc_info=True)
            continue

        if not hasattr(mod, "Plugin"):
            lg.debug(f"模块 {name} 非插件，跳过")
            continue

        # 在运行的插件
        plugin = mod.Plugin(con)

        if plugin.SLUG == "AbstractPlugin":
            plugin.SLUG = name

        # 检查冲突
        if plugin.SLUG in nameSet:
            lg.warning(f"插件 {name} SLUG({plugin.SLUG}) 重复，跳过")
            continue
        nameSet.add(plugin.SLUG)

        # 是否启用插件
        if config.has(plugin.SLUG) and "enable" in config.get(plugin.SLUG):
            if not config.get(plugin.SLUG)["enable"]:
                lg.info(f"插件 {name}-{plugin.ALIAS} 已被禁用")
                continue

        if issubclass(mod.Plugin, AbstractPlugin):
            lg.info(f"插件 {name}-{plugin.ALIAS} 加载成功 ")
            _plugins_query.append(plugin)

    def sort_priority(m):
        if hasattr(m, "PRIORITY"):
            return m.PRIORITY
        return 0

    _plugins_query.sort(key=sort_priority, reverse=True)
    _has_init = True


def get_plugins(con):
    global _plugins_query
    _plugins_query = []
    init_plugins(con)
    return _plugins_query


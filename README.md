# plugin-framework
插件式开发框架

### 工作机制如下：
1. 主程序调用 PluginManager.run_plugins 方法，并传入匹配词
2. 轮询每个可用插件，进行技能匹配，交给适合处理该指令的技能插件去处理。
#### 在第 2 步中，插件的轮询机制如下：
1. 在初始化阶段，依次扫描 plugins 目录、$HOME/.plugin-framework/contrib 目录和 $HOME/.plugin-framework/custom 目录下的可用插件。可用插件的判定标准为：
* 包含一个继承了 AbstractPlugin 基类的 Plugin 类；
* 在配置文件中没有将这个插件的 enable 设为 false。
2. 在扫描过程中，如果存在插件设置了 PRIORITY 属性，则对其优先级进行重排。默认都为 0，PRIORITY 值设得越大，则优先级越高。
3. 在轮询过程中，plugin-framework 会根据优先级逐个执行插件的 isValid() 方法，如果值为 True，则调用该插件的 handle() 方法进入处理。
### 我们可以先设计一个最简单的版本：

* 通过关键词 "打个招呼" 来触发这个插件响应；
* 无需任何配置项；
* 无需处理用户的指令，直接打印“hello world”。

### 这个最简单的版本实现如下：
```python
# -*- coding: utf-8-*-
from utils.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        print('hello world!')

    def isValid(self, text, parsed):
        return "打个招呼" in text
```
* 第2行：我们将插件的基类 utils.AbstractPlugin 引入；
* 第4行：我们编写一个名为 Plugin 的类，这个类集成了 AbstractPlugin 基类；
* 第6行和9行：我们分别实现了 AbstractPlugin 的两个接口 handle() 和 isValid() 。其中，isValid() 用于判断用户的指令是否适合交给这个插件处理；handle() 用于执行处理；
* 第10行，我们设置让用户的指令中包含了 “打个招呼” 关键词就执行响应。
### 解惑：为什么我的插件没有被触发？
#### 有几种可能：
1. 你的插件有 bug ，所以加载失败了；
2. 你的插件的 isValid() 方法与其他插件冲突，导致其他插件先被触发了
#### 对于第一种情况，最方便的做法是直接查看后台管理端的日志界面，不难看到有类似下面这样的日志：
```python
2023-08-04 17:36:11.640 | INFO     | utils.plugin_loader:init_plugins:68 - 插件 plugin1 加载成功 
2023-08-04 17:36:11.642 | INFO     | utils.plugin_loader:init_plugins:64 - 插件 plugin2 已被禁用
2023-08-04 17:36:11.643 | INFO     | utils.plugin_loader:init_plugins:68 - 插件 plugin3 加载成功
```
#### 如果你能在已激活插件中找到你的插件，说明插件加载成功。反之，说明插件加载失败。
# 一个简易的时间模块，包含常用的时间方法，仅支持python3

安装：

```
pip install python-time
```

使用方法，例如：

```
from pytime import time
print(pytime.timestamps())
```

输出：

```
1576225887
```

提供的所有方法：

```

pytime.timestamps()

pytime.microtime()

pytime.time_format(timestamp=None, format="%Y-%m-%d %X")

pytime.strtotime(format_time)

pytime.shift(time_type: str, timestamp: int=None)

pytime.sleep(second: int)

```

## Find it is easy!

这是一个快速寻找文件的Python库，帮助开发者寻找文件

## 快速开始

添加到你的项目中

```shell
pip install easyfind
```

或者正在使用uv?

```shell
uv add easyfind
```

立刻找到你的文件！

```python
from easyfind import find

path = find("foo.bar")

if path:
    print(path.absolute())
```

```stdout
/path/to/foo.bar
```

当然不止于此

```python
from easyfind import find, findall, finditer
from pathlib import Path

# 名字不确定？
tuple_name = find(("foo", "bar"))
list_name = find(["foo", "bar"])
set_name = find({"foo", "bar"})

# 可能有多个同名文件？
more_file = findall("foo.bar")

# 想要复杂的匹配规则？
end_with_py = find(lambda name: name.endswith("py"))

# 当然也支持从别的目录开始找！
# 别忘了符号链接
my_lib = find("libexample.so", root_dir=Path("/lib"), followlinks=True)

# 附赠生成器支持
for file in finditer("example"):
    print(file)
```

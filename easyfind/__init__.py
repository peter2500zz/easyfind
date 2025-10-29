import os
from pathlib import Path
from typing import Callable, Generator, Collection, TypeAlias


# 查找函数的签名
FindFunc: TypeAlias = Callable[[str], bool]

# 用迭代器节约内存
def finditer(
    match: str | FindFunc | Collection[str], 
    root_dir: Path = Path("."), 
    allow_dir: bool = False, 
    allow_file: bool = True, 
    followlinks: bool = False
) -> Generator[Path, None, None]:
    """
    遍历给定目录，寻找匹配的文件。

    Args:
        match (str | Callable[[str], bool] | Collection[str]): 匹配条件，可以是字符串、符合签名的匹配函数或字符串集合。
        root_dir (Path): 要开始搜索的根目录。
        allow_dir (bool): 是否匹配目录。
        allow_file (bool): 是否匹配文件。
        followlinks (bool): 是否跟随符号链接。

    Returns:
        Default (Generator[Path, None, None]): 将要遍历目录的迭代器。
    """

    # 名称不能重复
    # 顺便节约性能
    if isinstance(match, (list, tuple)):
        match = frozenset(match)

    for root, dirs, files in os.walk(root_dir, followlinks=followlinks):
        targets: list[str] = []

        if allow_dir:
            targets.extend(dirs)

        if allow_file:
            targets.extend(files)

        for target in targets:
            matched: bool = False

            # 优先判断最快的字符串
            if isinstance(match, str):
                if target == match:
                    matched = True
            else:
                if callable(match):
                    if match(target):
                        matched = True

                elif isinstance(match, Collection) and target in match:
                    matched = True

            if matched:
                yield Path(root) / target

def findall(
    match: str | FindFunc | Collection[str], 
    root_dir: Path = Path("."), 
    allow_dir: bool = False, 
    allow_file: bool = True, 
    followlinks: bool = False
) -> list[Path]:
    """
    遍历给定目录，返回所有匹配文件的路径。

    Args:
        match (str | Callable[[str], bool] | Collection[str]): 匹配条件，可以是字符串、符合签名的匹配函数或字符串集合。
        root_dir (Path): 要开始搜索的根目录。
        allow_dir (bool): 是否匹配目录。
        allow_file (bool): 是否匹配文件。
        followlinks (bool): 是否跟随符号链接。

    Returns:
        Default (list[Path]): 找到文件的路径列表。
    """

    return list(finditer(
        match,
        root_dir,
        allow_dir,
        allow_file,
        followlinks,
    ))

def find(
    match: str | FindFunc | Collection[str], 
    root_dir: Path = Path("."), 
    allow_dir: bool = False, 
    allow_file: bool = True, 
    followlinks: bool = False
) -> Path | None:
    """
    遍历给定目录，返回第一个匹配文件的路径。

    Args:
        match (str | Callable[[str], bool] | Collection[str]): 匹配条件，可以是字符串、符合签名的匹配函数或字符串集合。
        root_dir (Path): 要开始搜索的根目录。
        allow_dir (bool): 是否匹配目录。
        allow_file (bool): 是否匹配文件。
        followlinks (bool): 是否跟随符号链接。

    Returns:
        Default (Path | None): 如果存在一个或多个匹配的文件，返回第一个文件路径，没有则返回None。
    """

    return next(finditer(
        match,
        root_dir,
        allow_dir,
        allow_file,
        followlinks,
    ), None)

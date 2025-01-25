# -*- coding: utf-8 -*-
# @Time    : 2025/1/24 14:39
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_base_web_ui.py
# @Software: PyCharm


from web_ui.base_web_ui import BaseWebUi


def test1():
    """test1"""

    web_ui = BaseWebUi(
        is_debug=True,
        before_url="https://www.baidu.com"
    )
    web_ui.test()


def test2():
    """test2"""

    web_ui = BaseWebUi(
        is_debug=True,
        debugger_address=True
    )
    web_ui.test()


if __name__ == '__main__':
    test2()

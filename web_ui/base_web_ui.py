# -*- coding: utf-8 -*-
# @Time    : 2025/1/23 18:11
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : base_web_ui.py
# @Software: PyCharm


import os

from playwright.sync_api import sync_playwright


class BaseWebUi:
    """WebUi基类"""

    def __init__(
            self,
            is_debug: bool = False,
            headless: bool = False,
            debugger_address: bool = False,
            debugger_address_url: str = "http://127.0.0.1:9222",
            before_url: str = "",  # https://www.example.com
            width: int = None,
            height: int = None,
    ):
        """

        :param is_debug: 调试模式,浏览器不会直接执行`self.end()`关闭,需要手动键入`回车`后才会触发 self.end()
        :param headless: 是否使用无界面
        :param debugger_address: 是否操作已启动的浏览器
        :param debugger_address_url: 结合 `debugger_address` 使用
        :param before_url: 浏览器初始页面Url
        :param width: 浏览器初始宽
        :param height: 浏览器初始搞

        """

        # MACOS: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
        # Windows: ...

        self.is_debug = is_debug
        self.headless = headless
        self.debugger_address = debugger_address
        self.debugger_address_url = debugger_address_url
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.page_list = []
        self.page_list_len = None
        self.page_obj_list = []  # [{'index': 0, 'title': 'GitHub', 'url': 'https://github.com/'}...]
        self.before_url = before_url
        self.width = width
        self.height = height

    def browser_init(self):
        """
        浏览器初始化
        :return:
        """

        self.playwright = sync_playwright().start()

        if self.debugger_address:
            self.browser = self.playwright.chromium.connect_over_cdp(self.debugger_address_url)
            self.handle_context_page()
            self.reload_pages()
        else:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            if self.width and self.height:
                self.page.set_viewport_size({"width": self.width, "height": self.height})
            self.page.goto(self.before_url)
            self.show_title()

    def show_title(self):
        """输出当前页签"""

        self.out_logs(f"当前页签: {self.page.title()}")

    def show_context(self):
        """输出当前浏览器实例"""

        self.out_logs(f"当前浏览器: {self.context}")

    def set_windows_size(self, width, height):
        """浏览器界面尺寸"""

        self.page.set_viewport_size({"width": width, "height": height})

    def handle_context_page(self, ctx_index: int = 0, page_index: int = 0):
        """
        上下文切换
        :param ctx_index: 浏览器索引,默认情况下开启一个浏览器,默认是`0`
        :param page_index: 网页页签,通过索引切换进行操作,默认是`0`
        :return:
        """

        self.context = self.browser.contexts[ctx_index]
        self.show_context()
        self.browser_connet()
        self.page = self.context.pages[page_index]
        self.show_title()

    def reload_pages(self):
        """加载所有页签"""

        self.page_list = self.context.pages
        self.page_list_len = len(self.page_list)
        self.out_logs(f"当前页签数量: {self.page_list_len}")
        for index, page in enumerate(self.page_list):
            page_obj = {
                "index": index,
                "title": page.title(),
                "url": page.url,
            }
            self.out_logs(f"页签对象: {page_obj}")
            self.page_obj_list.append(page_obj)

    def browser_connet(self) -> bool:
        """获取浏览器连接状态"""

        result = self.browser.is_connected()
        self.out_logs(f"获取浏览器连接状态: {result}")
        return result

    @classmethod
    def code_gen(cls, url: str = "playwright codegen https://www.baidu.com", *args, **kwargs):
        """code_gen"""

        os.system(url)

    def out_logs(self, message: str):
        """out_logs"""

        print(message)
        ...

    def get_iframe(self, iframe_selector: str):
        """
        获取`iframe`实例, 对`iframe`内元素进行操作, 例如: iframe.query_selector(selector).click()
        :param iframe_selector:
        :return:
        """

        # 等待 iframe 加载完成
        iframe = self.page.wait_for_selector(iframe_selector).content_frame()
        iframe.wait_for_load_state()
        self.out_logs(f"iframe实例: {iframe}")
        return iframe

    @staticmethod
    def get_iframe_element(iframe_example, selector: str):
        """
        获取`iframe`内的元素, 结合 `self.get_iframe()` 使用
        :param iframe_example: `self.get_iframe()` 返回
        :param selector:
        :return:

        iframe_element.fill()
        iframe_element.click()
        ...
        """

        iframe_element = iframe_example.query_selector(selector)
        return iframe_element

    def start(self):
        """start"""

        self.browser_init()

    def end(self):
        """end"""

        if self.is_debug:
            input("输入回车后关闭浏览器...")

        self.browser.close()
        self.playwright.stop()

    def test(self):
        """test"""

        self.start()
        self.end()

    def demo(self):
        """demo"""

        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=self.headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.baidu.com")

#!/usr/bin/env python3
#coding:utf-8

from .base import FunctionalTest
import time


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        #edity访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        time.sleep(3)

        #她看到输入框完美的居中显示
        inputbox= self.get_item_input_box()
        inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


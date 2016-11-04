#!/usr/bin/env python3
#coding:utf-8

from .base import FunctionalTest
import time,sys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        #Edthy访问首页，不小心提交了一个空待办事项
        #输入框中没输入内容，她就按下了回车
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\ue007')
        time.sleep(2)

        #首页刷新了，显示了一个错误信息
        #提示待办事项不能为空
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item")

        #她输入一些文字，然后再次提交，这次没问题了
        self.get_item_input_box().send_keys('Buy milk\ue007')
        time.sleep(2)
        self.check_for_row_in_list_table('1: Buy milk')

        #她有点调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys("\ue007")
        time.sleep(2)

        #在清单页面她看到了一个类似的错误信息
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You can't have an empty list item")

        #输入文字后就没问题了
        self.get_item_input_box().send_keys("Make tea\ue007")
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        # self.fail('write me!')

    def test_cannot_add_duplicate_items(self):
        #Edity访问首页，新建一个清单
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\ue007')
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy wellies')

        #她一不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('Buy wellies\ue007')
        time.sleep(1)

        #她看到一条有帮助的错误信息
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")


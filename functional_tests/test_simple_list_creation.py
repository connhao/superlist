#!/usr/bin/env python3
#coding:utf-8

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time,sys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):

        #伊迪丝听说有一个很酷的在线待办事项应用
        #她去看了这个应用的首页
        self.browser.get(self.server_url)


        #他注意到网页的标题和头部都包含“To_Do”这个词
        self.assertIn('To-Do', self.browser.title)
        # self.assertIn('Django', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        #她在一个文本框中输入了“Buy peacock feathers” (购买孔雀羽毛)
        inputbox.send_keys('Buy peacock feathers')

        #她按回车键后，页面更新了
        #待办事项表格中显示了“1：Buy peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        #页面中又显示了一个文本框，可以输入其它待办事项
        #她输入了“Use peacock feathers to  make a fly”(使用孔雀羽毛做假蝇)
        #伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(2)

        #页面再次更新，她的清单中显示了两个待办事项
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        # self.assertIn('2: Use peacock feathers to make a fly',[row.text for row in rows])
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #现在一个叫做弗朗西斯的新用户访问了网站
        ##我们使用一个新浏览器会话
        ##确保伊迪丝的信息不会从cookie中泄漏出来
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #弗朗西斯输入一个新待办事项，新建一个清单
        #他不想伊迪丝那样新趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #这个页面还是没有edity的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)


        #两人都很满意，去睡觉了


#!/usr/bin/env python3
#coding:utf-8 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import unittest 

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox() 

    def tearDown(self):
        self.browser.quit() 

    def test_can_start_a_list_and_retrieve_it_later(self):

        #伊迪丝听说有一个很酷的在线待办事项应用 
        #她去看了这个应用的首页 
        self.browser.get('http://localhost:8000') 


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
        import time 
        time.sleep(2)

        table = self.browser.find_element_by_id('id_list_table') 
        rows = table.find_elements_by_tag_name('tr') 

        self.assertIn('1: Buy peacock feathers',[row.text for row in rows])

        #页面中又显示了一个文本框，可以输入其它待办事项 
        #她输入了“Use peacock feathers to  make a fly”(使用孔雀羽毛做假蝇)
        #伊迪丝做事很有条理 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly') 
        inputbox.send_keys(Keys.ENTER)

        time.sleep(3)

        #页面再次更新，她的清单中显示了两个待办事项
        table = self.browser.find_element_by_id('id_list_table') 
        rows = table.find_elements_by_tag_name('tr') 
        self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly',[row.text for row in rows])


        #伊迪丝想知道这个网站是否会记住她的清单 

        #她看到网站为她生成了唯一的URL 
        #而且页面中有一些文字解说这个功能 
        self.fail('Finish the test!') 

        #她访问那个URL，发现他的待办事项列表还在
        #她很满意，去睡觉了 


if __name__ == '__main__':
    unittest.main(warnings='ignore')


    




'''
browser = webdriver.Firefox() 
#伊迪丝听说有一个很酷的在线待办事项应用 
#她去看了这个应用的首页 
browser.get('http://localhost:8000') 

#他注意到网页的标题和头部都包含“To_Do”这个词
assert 'To-Do' in browser.title, "Browser title was " + browser.title 

#应用邀请她输入一个待办事项

#她在一个文本框中输入了“Buy peacock feathers” (购买孔雀羽毛)

#她按回车键后，页面更新了
#待办事项表格中显示了“1：Buy peacock feathers” 

#页面中又显示了一个文本框，可以输入其它待办事项 
#她输入了“Use peacock feathers” to  make a fly”(使用孔雀羽毛做假蝇)
#伊迪丝做事很有条理 

#页面再次更新，她的清单中显示了两个待办事项

#伊迪丝想知道这个网站是否会记住她的清单 

#她看到网站为她生成了唯一的URL 
#而且页面中有一些文字解说这个功能 

#她访问那个URL，发现他的待办事项列表还在

#她很满意，去睡觉了 

browser.quit() 

'''
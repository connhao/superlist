from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest 
from django.template.loader import render_to_string
from django.utils.html import escape
import time

from lists.views import home_page, view_list
from lists.models import Item, List
from lists.forms import ItemForm,EMPTY_LIST_ERROR

# Create your tests here.


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_render_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

    # def test_home_page_display_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #     request = HttpRequest()
    #     response = view_list(request)
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())


class NewListTest(TestCase):

    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        respose = self.client.get('/lists/%d/' % (correct_list.id))

        self.assertContains(respose, 'itemey 1')
        self.assertContains(respose, 'itemey 2')
        self.assertNotContains(respose, 'other list item 1')
        self.assertNotContains(respose, 'other list item 2')

    def test_save_a_POST_request(self):
        self. client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self. client.post(
                '/lists/new',
                data={'text': 'A new list item'}
        )

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'home.html',
        #     {'new_item_text': 'A new list item'}
        #     )
        # self.assertEqual(response.content.decode(), expected_html)
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
                '/lists/%d/' % (correct_list.id,),
                data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        #response = self.client.post('/lists/%d/' % (correct_list.id,))
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_from(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')


    def test_validation_errors_are_show_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new',data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
                '/lists/%d/' % (list_.id,),
                data={'text':''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))





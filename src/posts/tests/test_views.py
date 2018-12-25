from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.test import TestCase


from posts.models import Post
# Create your tests here.

class PostViewTestCase(TestCase):
    # our own method
    # all test cases methods hsould have the prefix 'test'
    def create_post(self, title='This title'):
        return Post.objects.create(title=title)
    
    def test_list_view(self):
        list_url = reverse('posts:list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view(self):
        obj = self.create_post(title='Another New Title Test')

        # Make sure if there is get_absolute_url method in the model
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, 200)
    
    def test_update_view(self):
        obj = self.create_post(title='Another New Title Test')

        # check the url pattern
        # If you test, the below statement does not work,
        # response = self.client.get(obj.get_absolute_url() + 'edit/')
        
        # In this case, try to use reverse method
        edit_url = reverse('posts:update', kwargs={"slug":obj.slug})
        # The above statement still return False.
        # So, we print edit_url, it is correct.
        print(edit_url)
        # The problem is from line 133 in views.py
        # based on the line, it should return 404
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_view(self):
        obj = self.create_post(title='Another New Title Test')
        # To use the below statement, add name parameter in delte url in urls.py
        # delete_url = reverse('posts:delete', kwargs={"slug":obj.slug}) 
        delete_url = obj.get_absolute_url() + 'delete/'
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 404)
# In testing model, we check if the fileds are correct
# for example, title or slug is correct after creating a model

# In testing form, what we will test is pretty much that data will be vaild
# if we pass other kinds of data, then data would be invalid

from django.utils.text import slugify
from django.test import TestCase
from django.utils import timezone

from posts.forms import PostForm
from posts.models import Post
# Create your tests here.

class PostFormTestCase(TestCase):
    def test_valid_form(self):
        title = 'A new title'
        slug='some-prob-unique-slug-by-this-test-abc-123'
        content = 'some content'
        obj = Post.objects.create(title=title, slug=slug, publish=timezone.now(), content= content)
        data = {'title': obj.title, "slug":obj.slug, 'publish': obj.publish, "content": content}
        form = PostForm(data=data) # PostForm(request.POST)
        self.assertTrue(form.is_valid()) # In order to use cleaned_data, we need to run form.is_valid() before testing with cleaned_data
        self.assertEqual(form.cleaned_data.get('title'), obj.title)
        self.assertNotEqual(form.cleaned_data.get('content'), "Another Item")
    
    def test_invalid_form(self):
        title = 'A new title'
        slug='some-prob-unique-slug-by-this-test-abc-123'
        content = 'some content'
        obj = Post.objects.create(title=title, slug=slug, publish=timezone.now(), content= content)
        data = {'title': obj.title, "slug":obj.slug, 'publish': obj.publish, "content": ""}
        form = PostForm(data=data) # PostForm(request.POST)
        self.assertFalse(form.is_valid()) 
        # print(form.errors)
        self.assertTrue(form.errors)


        


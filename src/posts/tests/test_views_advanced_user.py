from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.test import TestCase, RequestFactory # built-in factory for creating a request

from posts.models import Post
from posts.views import post_update, post_create
# Create your tests here.

User = get_user_model()

class PostViewAdvanceTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
                        username='abc123test123',
                        email='abc123test123@gmail.com',
                        password='pwtest123#$$$',
                        is_staff = True,
                        is_superuser = True
                    )

    # our own method
    # all test cases methods hsould have the prefix 'test'
    def create_post(self, title='This title'):
        return Post.objects.create(title=title)

    def test_user_auth(self):
        obj = self.create_post(title='Another New Title Test')
        edit_url = reverse('posts:update', kwargs={"slug":obj.slug})
        request = self.factory.get(edit_url)
        request.user = self.user

        # we need to grab the view and pass this fake request in here
        # so we're developing our own request in this test
        # and then we need to create a response to it so we actually need
        # to import our view
        response = post_update(request, slug=obj.slug)

        self.assertEqual(response.status_code, 200)
        # print(request.user.is_authenticated())

    def test_user_post(self):
        request = self.factory.post("/posts/create")
        request.user = self.user
        response = post_create(request)
        self.assertEqual(response.status_code, 200)
    
    # test an empty page
    def test_empty_page(self):
        page = '/adsfasdf/asdfasdfasdf'
        request = self.factory.get(page)
        request.user = self.user
        response = post_create(request)
        self.assertEqual(response.status_code, 200)
    
    def test_unauth_user(self):
        obj = self.create_post(title='Another New Title Test')
        edit_url = reverse('posts:update', kwargs={"slug":obj.slug})
        request = self.factory.get(edit_url)
        request.user = AnonymousUser()
        response = post_update(request, slug=obj.slug)
        # response = PostUpdateView.as_view(request) # it is for Class-Based View
        # needed to change line 134, if it is raising Http404, it does not giving us 
        # the response status code. Thus, need to change the part of code, and return response
        # it is using for test purpose
        print(response)
        self.assertEqual(response.status_code, 404)
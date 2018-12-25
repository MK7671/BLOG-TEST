# The file name is changed from tests.py to test_models.py
# and it is in created folder called "tests"
# After created "tests" directory, and create __init__.py file
# and moved test_models.py in the directory

# test_ is how Django will recognize that your test file is actually there and 
# then that's the same as true with the actual methods inside of the test case itself
from django.utils.text import slugify
from django.test import TestCase


from posts.models import Post
# Create your tests here.

class PostModelTestCase(TestCase):
    # built-in method
    # we can actually create the test version of this item in the test database
    # It is not gonna be in our actual database
    def setUp(self):
        Post.objects.create(title="A new title",
                            slug='some-prob-unique-slug-by-this-test-abc-123')
    
    # our own method
    # all test cases methods hsould have the prefix 'test'
    def create_post(self, title='This title'):
        return Post.objects.create(title=title)
    
    # Create test case
    # When you run your tests, the default behavior of the test utility is to 
    # find all the test cases (that is, subclasses of unittest.TestCase) in any file WHOSE NAME BEGINS WITH TEST, 
    # automatically build a test suite out of those test cases, and run that suite.
    
    def test_post_title(self):
        obj = Post.objects.get(slug='some-prob-unique-slug-by-this-test-abc-123')
        self.assertEqual(obj.title, "A new title")
        self.assertTrue(obj.content == "") # maybe I want to change
        # self.assertTrue(100 == 40 + 2000)

    def test_post_slug(self):
        # generate slug
        title1 = 'another title abc'
        title2 = 'another title abc2'
        title3 = 'another title abc'
        slug1 = slugify(title1)
        slug2 = slugify(title2)
        slug3 = slugify(title3)
        obj1 = self.create_post(title=title1)
        obj2 = self.create_post(title=title2)
        obj3 = self.create_post(title=title3)
        # print(obj2.slug)
        # print(obj3.slug)
        
        self.assertEqual(obj1.slug, slug1)
        self.assertEqual(obj2.slug, slug2)
        
        self.assertNotEqual(obj3.slug, slug3)
        self.assertNotEqual(obj2.slug, 'False')

    def test_post_qs(self):
        title = 'another title abc'
        obj1 = self.create_post(title=title)
        obj2 = self.create_post(title=title)
        obj3 = self.create_post(title=title)
        qs = Post.objects.filter(title=title)

        # should have unique title, but in this model, it is not set up like that
        # so the below statement will return True
        self.assertEqual(qs.count(), 3)

        # unique slug
        qs2 = Post.objects.filter(slug=obj1.slug)
        self.assertEqual(qs2.count(), 1)

        

    # In bash, test by typing "python manage.py test posts"

from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post

class PostApiTestCase(TestCase):
    def setUp(self):
        # Creates two test users and assigns them to self.u1 and self.u2
        self.u1 = get_user_model().objects.create_user(
            email="test@example.com", password="password"
        )

        self.u2 = get_user_model().objects.create_user(
            email="test2@example.com", password="password2"
        )
        # Creates two Post objects. 
        # It creates a dictionary with a mapping between each 
        # post’s ID and the object so we can look up the Post by ID later (post_lookup).
        posts = [
            Post.objects.create(
                author=self.u1,
                published_at=timezone.now(),
                title="Post 1 Title",
                slug="post-1-slug",
                summary="Post 1 Summary",
                content="Post 1 Content",
            ),
            Post.objects.create(
                author=self.u2,
                published_at=timezone.now(),
                title="Post 2 Title",
                slug="post-2-slug",
                summary="Post 2 Summary",
                content="Post 2 Content",
            ),
        ]

        # let us look up the post info by ID
        self.post_lookup = {p.id: p for p in posts}

        # override default test client, with APIClient
        self.client = APIClient()
        # Inserts a Token object into the database (which generates a key for authentication). The Token is for the u1 user.
        token = Token.objects.create(user=self.u1)
        # Sets the credentials() of the APIClient client to use the token in the HTTP Authorization header.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    # Queries the Post objects that were inserted in setUp(), 
    # using the API, and then checks that their data matches what we expect.
    def test_post_list(self):
        resp = self.client.get("/api/v1/posts/")
        # adapt for pagnation, get from ["results"] 
        # This does not work for pagnated pages, PAGE_SIZE=1
        data = resp.json()["results"]
        #data = resp.json()
        self.assertEqual(len(data), 2)
        # verify count per page instead
        # # •	count: The total number of records available
        #self.assertEqual(resp.json()["count"], 2)
        

        # post_dict is dict representation of post model, deserialised by json
        for post_dict in data:
            post_obj = self.post_lookup[post_dict["id"]]
            self.assertEqual(post_obj.title, post_dict["title"])
            self.assertEqual(post_obj.slug, post_dict["slug"])
            self.assertEqual(post_obj.summary, post_dict["summary"])
            self.assertEqual(post_obj.content, post_dict["content"])
            # endswith allows for different server signatures, endswith api
            self.assertTrue(
                post_dict["author"].endswith(f"/api/v1/users/{post_obj.author.email}")
            )
            self.assertEqual(
                post_obj.published_at,
                datetime.strptime(
                    post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=UTC),
            )
    
    # what happens if an unauthenticated user tries to create a Post. 
    # In order to simulate an unauthenticated user we call 
    # credentials() on the client with no arguments, 
    # which removes the saved Authorization header.
    def test_unauthenticated_post_create(self):
        # unset credentials so we are an anonymous user
        self.client.credentials()
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/test@example.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        # 401 for unauthenticated
        self.assertEqual(resp.status_code, 401)
        # check that no new post is created, 
        # count is still 2 as by setUp()
        self.assertEqual(Post.objects.all().count(), 2)    
    
    # creates a Post through the API, then queries the database 
    # for it using the id that was returned. 
    # It then checks that the data in the database matches what was posted.
    def test_post_create(self):
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/test@example.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        # then queries the database for it using the id that was returned.
        post_id = resp.json()["id"]
        post = Post.objects.get(pk=post_id)
        self.assertEqual(post.title, post_dict["title"])
        self.assertEqual(post.slug, post_dict["slug"])
        self.assertEqual(post.summary, post_dict["summary"])
        self.assertEqual(post.content, post_dict["content"])
        self.assertEqual(post.author, self.u1)
        self.assertEqual(post.published_at, datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC))
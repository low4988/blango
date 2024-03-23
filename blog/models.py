from django.db import models
from django.conf import settings
from django.contrib import admin

'''
To use the class in our ForeignKey, we need use the Django settings model. 
Verify that you have from django.conf import settings at the top of the file.
'''
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here. # also remebet to register model, in admin.py

'''
Create a profile model only for authors, i.e optional to user model
with OneToOneField relation to users in AUTH_USER_MODEL
AuthorProfile, to store a user's biography text.
'''
class AuthorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField()

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"

class Tag(models.Model):
  # It’s simple and just contains a single field for value.
    value = models.TextField(max_length=100)

    def __str__(self):
        return self.value

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
'''
Creating a Comment model. 
It should have a creator field to store the user who created it, 
plus fields to store the created time and modified time. 
Don't forget the generic relationship fields.
before Post class
'''
class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # added dbindexing object_id
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    # added dbindexing created_at
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)





class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add, when a post is saved its creation date and time will be set automatically
    modified_at = models.DateTimeField(auto_now=True) # auto_now set to True, which means it will be set to the current date and time whenever a Post is saved.
    #published_at = models.DateTimeField(blank=True, null=True)
    # use database index to speed up filtering and ordering on this column
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    title = models.TextField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField() # stored as plain HTML, This is not the most secure approach, so it’s only advisable if you trust your authors not to add malicious HTML. If you’re building a site that will output user-supplied HTML, consider using something like Bleach to remove unsafe HTML.
    tags = models.ManyToManyField(Tag, related_name="posts")

    comments = GenericRelation(Comment) # argument Comment class

    def __str__(self):
        return self.title

'''
Author Foreign Key
The author is a ForeignKey to settings.AUTH_USER_MODEL: 
a Django setting which is a string. 
ForeignKey can be used either by passing the class itself, 
or passing a string which is parsed to load and refer to the class. 
By passing settings.AUTH_USER_MODEL, we’ll be able to change the model class 
that’s used for authentication by updating the Django settings, 
and all models that refer to this setting will update automatically 
to use the right model. By default, the value is auth.
User, which refers to the User model in the Django auth application.

Add a comments GenericRelation field on Post back to Comment. 
This will make it easier to find comments for a post.
'''



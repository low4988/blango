from django.db import models
from django.conf import settings
'''
To use the class in our ForeignKey, we need use the Django settings model. 
Verify that you have from django.conf import settings at the top of the file.
'''

# Create your models here.

class Tag(models.Model):
  # It’s simple and just contains a single field for value.
    value = models.TextField(max_length=100)

    def __str__(self):
        return self.value

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add, when a post is saved its creation date and time will be set automatically
    modified_at = models.DateTimeField(auto_now=True) # auto_now set to True, which means it will be set to the current date and time whenever a Post is saved.
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField() # stored as plain HTML, This is not the most secure approach, so it’s only advisable if you trust your authors not to add malicious HTML. If you’re building a site that will output user-supplied HTML, consider using something like Bleach to remove unsafe HTML.
    tags = models.ManyToManyField(Tag, related_name="posts")

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
'''
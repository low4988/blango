from rest_framework import generics

from blog.api.serializers import PostSerializer
from blog.models import Post

# set permissions for view by rest_framework.permissions
# note IsAdminUserForObject inherits permissions.IsAdminUser, 
# and subclasses with has_object_permission, not to be used directly
from blog.api.permissions import AuthorModifyOrReadOnly
from blog.api.permissions import IsAdminUserForObject

# get() method that calls list() provided by 
# ListCreateAPIView
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# get(), put() , delete() methods already provided by 
# RetrieveUpdateDestroyAPIView.
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # set detail view permissions with class in blog.api.permission file
    # use subclassing
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer

'''
However IsAdminUser always returns True from 
has_object_permission(), 
even if a user isn't logged in! 

So by using it we'll give all permissions to everyone.

We can solve this by subclassing IsAdminUser 
and implementing has_object_permission():
| or
permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

DRF does not know about your objects, 
so it does not have a way of checking permissions. 
Therefore, IsAdminUser will always return True. 

By subclassing IsAdminUser, 
you can create a method that corresponds to your object.

DRF will not issue an error message if you do not subclass IsAdminUser. 
This method already returns a boolean value.
'''
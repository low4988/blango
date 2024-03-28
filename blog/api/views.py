from rest_framework import generics

from blog.api.serializers import PostSerializer
from blog.models import Post

# get() method that calls list() provided by 
# ListCreateAPIView
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# get(), put() , delete() methods already provided by 
# RetrieveUpdateDestroyAPIView.
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
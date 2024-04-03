# generics
from rest_framework import generics
# viewsets
from rest_framework import viewsets
# for Post views
from blog.api.serializers import PostSerializer, PostDetailSerializer
from blog.models import Post
# for User views
from blango_auth.models import User
from blog.api.serializers import UserSerializer

# viewsets, tagviewset
from blog.api.serializers import TagSerializer
from blog.models import Tag

from rest_framework.decorators import action
from rest_framework.response import Response

# cacheing generics with method_decorator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied

# set permissions for view by rest_framework.permissions
# note IsAdminUserForObject inherits permissions.IsAdminUser, 
# and subclasses with has_object_permission, not to be used directly
from blog.api.permissions import AuthorModifyOrReadOnly
from blog.api.permissions import IsAdminUserForObject

# TagViewSet
# @action, decorator to indicate that a URL should be set up for it
# methods: A list of HTTP methods that the action will respond to. Defaults to ["get"].
# detail: Required, apply to detail requests (if True) or list (if False). 
# url_path: Manually specify the path to be used in the URL. Defaults to the method name (e.g. posts).
# url_name: Manually specify the name of the URL pattern. Defaults to the method name with underscores replaced by dashes. The full name of our method’s URL is tag-posts.
# name: A name to display in the Extra Actions menu in the DRF GUI. Defaults to the name of the method.

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=["get"], detail=True, name="Posts with the Tag") 
    def posts(self, request, pk=None):
        # get pk for tag - get_object()
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)

    @method_decorator(cache_page(300))
    def list(self, *args, **kwargs):
        return super(TagViewSet, self).list(*args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, *args, **kwargs):
        return super(TagViewSet, self).retrieve(*args, **kwargs)

# combine all post methods into one view-set
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    # split depending on method, list and create. 
    # Previously separate classes
    def get_serializer_class(self):
        if self.action in ("create"): #("list", "create"): # must remove list here?
            return PostSerializer
        return PostDetailSerializer
    
    @method_decorator(cache_page(120))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)

    # cacheing page,
    @method_decorator(cache_page(300)) # 300sec
    @method_decorator(vary_on_headers("Authorization", "Cookie")) # check headers, update if change, regardles of cache time
    #@method_decorator(vary_on_cookie) # idiotic "shortcut" for vary_on_headers("Cookie")
    #mine get detail false, -> return list by request.user pk
    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = self.get_queryset().filter(author=request.user)
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)
'''
old separate views

# get() method that calls list() provided by 
# ListCreateAPIView
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# get(single), put() , delete() methods already provided by 
# RetrieveUpdateDestroyAPIView.
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # set detail view permissions with class in blog.api.permission file
    # use subclassing
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    
    queryset = Post.objects.all()
    # new serializer_class
    #serializer_class = PostSerializer # old
    serializer_class = PostDetailSerializer
'''

# new HyperlinkedRelatedField, lookup_field = "email"
class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
        return super(UserDetail, self).get(*args, *kwargs)    


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
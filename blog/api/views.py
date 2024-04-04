# FilterSet
from blog.api.filters import PostFilterSet
# queryset filters, Keyword argument queries – in filter(),
from django.db.models import Q
from django.utils import timezone
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

# /api/v1/tags/
# pagnation only in fullscreen by arrow
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=["get"], detail=True, name="Posts with the Tag") 
    def posts(self, request, pk=None):
        # get pk for tag - get_object()
        tag = self.get_object()
        # check if multiple pages, as per PAGE_SIZE
        page = self.paginate_queryset(tag.posts)
        if page is not None:
            post_serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(post_serializer.data)
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

#/api/v1/posts/
# combine all post methods into one view-set
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    # filter standard fields defined in filterset meta class
    # Custom fields possible, in PostFilterSet
    filterset_class = PostFilterSet 
    #replaced by filterset class
    # filters by field, in page filter
    #filterset_fields = ["author", "tags"]

    # filter Ordering 
    ordering_fields = ["published_at", "author", "title", "slug"]
    
    # we'll still refer to this in `get_queryset()`
    queryset = Post.objects.all()

    # unfiltered queryset still availble for Serialisers
    # get_queryset() method applies to all the API action methods.

    # filter response queryset with get_queryset() method, here based on user
    # get_queryset() method takes no arguments, 
    # so use attributes/properties that are set on self (e.g. request.user). 
    # also kwargs setup in path "/<str:period_name>/", by self.kwargs.get("period_name")
    def get_queryset(self):
        if self.request.user.is_anonymous:
            # published only
            return self.queryset.filter(published_at__lte=timezone.now())

        if not self.request.user.is_staff:
            # allow all
            return self.queryset

        # filter for own or | published
        # implicit authenticated non-staff
        return self.queryset.filter(
            Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
        )
        # filters are “AND”ed together. Use Q objects for more complex queries, e.g. queries with OR statements
        # A Q object (django.db.models.Q) is an object used to encapsulate 
        # a collection of keyword arguments. These keyword arguments are specified as in “Field lookups”
        
        # further filtering, to request.user
        # filter by keyword in path, "/<str:period_name>/". in blog/api/urls.py
        time_period_name = self.kwargs.get("period_name")

        # no name given
        if not time_period_name:
            # no further filtering required
            return queryset

        if time_period_name == "new":
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(hours=1)
            )
        elif time_period_name == "today":
            return queryset.filter(
                published_at__date=timezone.now().date(),
            )
        elif time_period_name == "week":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
        else:
            raise Http404(
                f"Time period {time_period_name} is not valid, should be "
                f"'new', 'today' or 'week'"
            )   

    # split depending on method, list and create. 
    # Previously separate classes
    def get_serializer_class(self):
        if self.action in ("create"): #("list", "create"): # must remove list here?
            return PostSerializer
        return PostDetailSerializer
    
    
    # Since the list of Posts now changes with each user, we need to make sure we add the vary_on_headers() decorator to it, with Authorization and Cookie as arguments:
    @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers("Authorization", "Cookie"))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)

    # cacheing page,

    #@method_decorator(vary_on_cookie) # idiotic "shortcut" for vary_on_headers("Cookie")
    #mine get detail false, -> return list by request.user pk
    # filtering,applies to all API action methods. 
    # self.get_queryset().get(pk=pk) rather than Post.objects.get(pk=pk)
    @method_decorator(cache_page(300)) # 300sec
    @method_decorator(vary_on_headers("Authorization", "Cookie")) # check headers, update if change, regardles of cache time
    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = self.get_queryset().filter(author=request.user)
        
        # pagination
        # self.paginate_queryset() part of generic view and viewsets
        # first instantiate with self.paginate_queryset(queryset) , If no paginator is set up (on the class or in the settings), then this method will return None
        page = self.paginate_queryset(posts)
        # Check if there is a need for multiple pages, list returned
        # instance is None if returned queryset is less than PAGE_SIZE
        if page is not None:
            # Create serializer with all pages, pass this serialiser.data to get_paginated_respons
            serializer = PostSerializer(page, many=True, context={"request": request})
            # get_paginated_response() returns a Response
            # this pagnated response is returned as a page with results
            # results: An array of objects on this page. 
            # This is the equivalent of the body of the response that was sent 
            # when pagination was not enabled.
            return self.get_paginated_response(serializer.data)
        
        # If paginate_queryset() returns None, 
        # fall back to your original method of generating a response, 
        # by passing the entire queryset to the serializer
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
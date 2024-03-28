from django.urls import path, include
# allows pattern to define response file type in suffix .json
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import PostList, PostDetail

from rest_framework.authtoken import views

urlpatterns = [
    path("posts/", PostList.as_view(), name="api_post_list"),
    # path without trailing <int:pk>/ will not load html only .json
    path("posts/<int:pk>/", PostDetail.as_view(), name="api_post_detail"),
]
# path("posts") views, PostList/Detail.as_view() decorated directly
urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token)
]
urlpatterns = format_suffix_patterns(urlpatterns)


from django.urls import path, include, re_path # re_path for swagger
# allows pattern to define response file type in suffix .json
from rest_framework.urlpatterns import format_suffix_patterns

# Post api views
from blog.api.views import PostList, PostDetail

# User api views
from blog.api.views import UserDetail
# REST_FRAMEWORK
from rest_framework.authtoken import views

# Swagger UI DRF, note django.urls.re_path above
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os
# swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    # note wrong address provided, .codio.io/api/v1/ -> codio-box.uk/api/v1
    # url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/", 
    # copy from terminal instead, https://mangoaccent-torchepisode-8000.codio-box.uk/api/v1/
    url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio-box.uk/api/v1/",

    
    public=True,
)


# path Posts views, PostList/Detail.as_view() decorated directly
urlpatterns = [
    path("posts/", PostList.as_view(), name="api_post_list"),
    # path without trailing <int:pk>/ will not load html only .json
    path("posts/<int:pk>/", PostDetail.as_view(), name="api_post_detail"),
]

# path User views
urlpatterns += [
# note urlpattern users/<str:email> without trailing / else looup with / at end
path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]


urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
]

# swagger patterns 
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

# not metioned in tutorial
# remove format_suffix_patterns as defined by swagger, r"^swagger(?P<format>\, else fromat defined more than once
# django.core.exceptions.ImproperlyConfigured: "^swagger(?P<format>\.json|\.yaml)\.(?P<format>[a-z0-9]+)/?$" is not a valid regular expression: redefinition of group name 'format' as group 2; was group 1 at position 39
#urlpatterns = format_suffix_patterns(urlpatterns)
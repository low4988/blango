"""blango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
''' without DjDT toolbar
from django.contrib import admin
from django.urls import path
'''
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# user registration
from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm

# user accounts authentication and registration
import blango_auth.views
urlpatterns = [
    # 'include', redirects all accounts/ requests to 
    # path django.contrib.auth.urls with accounts/ chopped of
    # accounts/login -> path ('login', url) in other file
    # accounts/logout -> path ('logot', url) in other "django.contrib.auth.urls"
    # both refer to "accounts/", sub file /urls different use django_registration.backends.activation.urls
    
    path("accounts/", include("django.contrib.auth.urls")),
    # This rule must come after the mapping from accounts/ , first will have precedence
    # to include("django.contrib.auth.urls"), since both sets of URLs define some of the same rules (for example, login/),This rule must come after the mapping from accounts/ to include("django.contrib.auth.urls"), since both sets of URLs define some of the same rules (for example, login/),
    path("accounts/", include("allauth.urls")),
    
    path("accounts/profile/", blango_auth.views.profile, name="profile"),
    path("accounts/register/",
    # RegistrationView for BlangoRegistrationForm
    RegistrationView.as_view(form_class=BlangoRegistrationForm),
    name="django_registration_register",),  
    # mapping to include the two step activation URLs
    path("accounts/", include("django_registration.backends.activation.urls")),
]


# other imports
import blog.views
urlpatterns += [
    path('admin/', admin.site.urls),
]

# API interface urls
# /v1/ for versioning, will allow us to implement changes to
# the API without breaking backwards-compatibility with older clients.
urlpatterns += [
    path("api/v1/", include("blog.api_urls")),
]

# note += extending default urlpatterns
'''
Add a route for "" (empty string) to this view in urls.py. 
path for "" empty request -> index.html, if no subpath is added, i.e ""

Don't forget to also import the views file. (above)

'''
# for DjDT toolbar, only active if DEBUG==True
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    # other patterns
    path("", blog.views.index)
]

urlpatterns += [
    # other patterns
        path("post/<slug>/", blog.views.post_detail, name="blog-post-detail")
]
urlpatterns += [
    # other patterns
        path("ip/", blog.views.get_ip)
]
# delete after testing
#from django.conf import settings
#print(f"Time zone: {settings.TIME_ZONE}")
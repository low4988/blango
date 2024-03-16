from django.shortcuts import render
from django.utils import timezone # for timezone in Post.objects
from blog.models import Post

# Create your views here.

# renders blog index.html, 
# blog/index.html extends base.html
#def index(request):
#    return render(request, "blog/index.html")

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})

'''
Note the use of the published_at__lte=timezone.now() filter. 
This means we'll only load 
Post objects that have been published (have a publication date in the past).
'''

from django.utils import timezone # for timezone in Post.objects
from blog.models import Post
from django.shortcuts import render, get_object_or_404

# Create your views here.

# renders blog index.html, 
# blog/index.html extends base.html
#def index(request):
#    return render(request, "blog/index.html")

''' index
Note the use of the published_at__lte=timezone.now() filter. 
This means we'll only load 
Post objects that have been published (have a publication date in the past).
'''
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, "blog/index.html", {"posts": posts})


''' post_detail
fetching a Post using its slug. 
get_object_or_404 shortcut will automatically return a 
# 404 Not Found response 
if the requested object isn't found in the database:
'''
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {"post": post})
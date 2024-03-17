
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

# 1.18.1 Crispy form update, albait non-Crispy example

First, we check if the user is active. 
Users who are inactive or aren’t logged in (anonymous users) will fail this test and default to having the comment_form variable set to None.

If is_active, we check the request method. 
If it's not POST, a blank CommentForm is created.

If it is a POST, then we create the 
CommentForm using the posted data. 

Then, if comment_form.is_valid(), 
save the form, using the commit=False argument. 
Return Comment, instead of write object to the database 

The attributes we set are the 
content_object (the current Post being viewed); 
and then return it. 

We need to do this to set the other attributes on the 
Comment before saving. 
Creator (the current logged in user). 

The Comment is then saved, and finally, 
we perform a redirect back to the current Post 
(this essentially just refreshes the page for the user 
so they see their new comment).

We have to also adjust the render call at the end of the view 
to include the comment_form variable:

And finally, make sure to import redirect from django.shortcuts and 
CommentForm from blog.forms at the start of the file.
'''
from django.shortcuts import redirect
from blog.forms import CommentForm

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    #return render(request, "blog/post-detail.html", {"post": post})

    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    
    return render(
        request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )
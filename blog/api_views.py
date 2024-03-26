import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post

# JsonResponse only returns dict objects, 
# convert post QuerySet to dict
# called with JsonResponse(post_to_dict(post))
def post_to_dict(post):
    return {
        "pk": post.pk,
        "author_id": post.author_id,
        "created_at": post.created_at,
        "modified_at": post.modified_at,
        "published_at": post.published_at,
        "title": post.title,
        "slug": post.slug,
        "summary": post.summary,
        "content": post.content,
    }
'''
# Django will reject POST, PUT and DELETE requests that don't 
# include a CSRF token, unless the view is marked as not requiring one. 
# With the django.views.decorators.csrf.csrf_exempt decorator.
# specifically designing views for use with a REST API 
# we would expect to have some other method of authenticating 
# the user and requests, so CSRF protection is not really required.
'''

# Handle different request methods by checking
# request.method == "GET", type of method
@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        posts_as_dict = [post_to_dict(p) for p in posts]
        return JsonResponse({"data": posts_as_dict})
    elif request.method == "POST":
        post_data = json.loads(request.body)
        post = Post.objects.create(**post_data)
        return HttpResponse(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )
    # Note allowed methods ["GET", "POST"], 
    # other methods get NotAllowed response
    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        return JsonResponse(post_to_dict(post))
    elif request.method == "PUT":
        post_data = json.loads(request.body)
        for field, value in post_data.items():
            setattr(post, field, value)
        post.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    # Note allowed methods ["GET", "POST", "DELETE"], 
    # other methods get NotAllowed response
    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
from django.contrib.auth import get_user_model
user_model = get_user_model()

'''
Before the template filter can be used, it needs to be registered into the template library. 
This is actually a three step process:
1.Import the django template module.
2.Create an instance of the django.template.Library class.
3.Register the filter function into the Library with its filter function.
'''

from django import template
register = template.Library()
# Convention is to call this Library instance variable 'register', 
# it makes it clear that the decorator is registering a filter.
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#registering-custom-filters

'''
The Library.filter() method takes two arguments:

The name of the filter - a string.
The compilation function - a Python function (not the name of the function as a string).

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter
def lower(value):
    return value.lower()

If you leave off the name argument, as in the second example above, 
Django will use the function's name as the filter name.
'''
'''
naive version

@register.filter # register.filter(<filter_name_>, <filter_function>)
def author_details(author):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"
    
    if author.email:
        email = author.email
        prefix = f'<a href="mailto:{email}">'
        suffix = "</a>"
    else:
        prefix = ""
        suffix = ""

    return f"{prefix}{name}{suffix}"
'''
# these functions are included in format_html
#from django.utils.html import escape
#from django.utils.safestring import mark_safe

from django.utils.html import format_html

@register.filter
def author_details(author, current_user):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)


''' 
{#% extends "base.html" %#} <!-- existing line -->
{#% load blog_extras %#} # this is the new filter_function, 
same name as file in <appname> / <templatetags> / blog_extras 

{#% load blog_extras %#} # extra # in {#%

Django looks for template libraries to load inside Python files in the 
templatetags folder inside Django apps. 
The template library it loads is simply the name of the file
<appname> / <templatetags> / blog_extras , __init__.py file # both empty
'''

'''

Make sure the function is decorated with @register.simple_tag. 

define a row function that returns the HTML for opening a row. 
define a endrow function that returns HTML for closing a row.

By default, the simple_tag function uses the name of the 
function as the template tag's name, 
but like the filter registration function, it can accept 
-a name argument to customize the name of the 
tag in templates.

To be safe, simple tags automatically escape their output, 
so the tags are not being rendered properly. 
format_html('<div class="row">')
'''

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

# note same markup as endrow() but, more explicit to follow with tag pair
@register.simple_tag
def endcol():
    return format_html("</div>")

from blog.models import Post
'''inclusion_tag, depends on blog.models Post
 Creates a context ,dict, to hand in to template
 
 It then fetches the five most recent Post objects 
 (ordered by published_at), 
 but excludes the Post that was passed in 
 (because we want to show recent posts that aren*t the Post being viewed)
 
 The template tag function returns a dictionary 
 with the posts in the posts key 
 and the string Recent Posts in the title key 
 this will be the context data that Django uses to render the template.

exclude() 
Returns a new QuerySet containing objects that do not match 
the given lookup parameters.
'''
@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}
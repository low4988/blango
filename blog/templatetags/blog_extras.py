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



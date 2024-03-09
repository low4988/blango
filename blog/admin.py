from django.contrib import admin

# Register your models here.

# Let’s start by looking at the simplest method of registering
# a model. We’ll do this with the Tag model. 
# First our model needs to be imported into the admin.py file:

from blog.models import Tag, Post, Comment

# Register your models here. # Any chang to model requires migration to take effect
admin.site.register(Tag)
# admin.site.register(Post, PostAdmin) # registered below, after definition of PostAdmin
admin.site.register(Comment)

'''
To configure how the admin site behaves with a certain model, 
a subclass of admin.ModelAdmin must be created. 
This subclass’s attributes determine how the model is displayed. 
First let’s look at how we’ll create one, for the Post model.
'''

class PostAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {"slug": ("title",)} # prepop not displayedb by default, noneditable
    list_display = ('slug', 'published_at') # display also autopopulated fields

#Now that the PostAdmin class is defined, 
#let’s return to the register function. 
#The PostAdmin class is passed as the second argument:

admin.site.register(Post, PostAdmin)

'''
Here we’re setting just one attribute, prepopulated_fields. 

When used in this way, 
some JavaScript is inserted into the admin page 
so that the slug field updates when the title field changes. 
It will automatically “slugify” the title. 
But, there are many other ways to customise the ModelAdmin. 
Some of the more common customizations are:

exclude: 
a list of fields to disallow editing of in the admin.
For example, we might want to prevent users from 
manually setting the slug, and instead compute it when 
saving the Model. 
In which case, we would set exclude to ["slug"].

fields: 
this works the opposite way to exclude. 
If set, only fields in the fields list will be editable. 
Note that if a field requires a value, but is not editable 
(either by the use of exclude or fields), 
then saving the model instance will fail because 
the field will not be valid.

list_display: 
a list of fields to include in the admin page list view. 
For example, we might want to see both a Post’s title, and when it was published. 
We would do this by setting 
list_display to ["title", "published-at"].
'''
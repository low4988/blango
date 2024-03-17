from django import forms

from blog.models import Comment

''' standard
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

'''

'''
# Crispy with FormHelper for options
https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

FormHelper is imported from crispy_forms.helper. 
To use it, we should implement a form's__init__ method 
and have it assign self.helper to a FormHelper instance. 
For our CommentForm, after doing that, it would look like this:

# 1.19 crispy helper layout
Since we're just posting the form to the same page on which it was loaded, 
we don't actually need to set any of the FormHelper attributes. 
But we will use the FormHelper.add_input() method to add the submit button.

Then, we'll instantiate them and add it to the form in one go. 
Add this inside the __init__ method.
https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
'''

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
'''
-form_method: Set the form method, GET or POST. 
It defaults to POST. 
If set to POST, then the crispy template tag will automatically 
render the CSRF token in the form.  # cross site request forgery
https://docs.djangoproject.com/en/5.0/howto/csrf/
https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html

-form_action: If you want the form to submit to a different page than the one on which it was loaded, 
you can set the URL, path, or URL name to this attribute.

-form_id: The value to set as the id attribute of the <form> tag.
-form_class: The value to set as the class attribute of the <form> tag.
-attrs: A dictionary of attributes to set on the <form> tag.

As well as setting attributes, we can also add extra inputs. 
Most of the time, you'd just use this to add a submit button to your form.
'''
from rest_framework import permissions


class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # either SAFE_METHODS (GET, HEAD and OPTIONS)
        # or user making request is same as object author
        # evaluate True
        return request.user == obj.author

class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        # if both request.user and request.user.is_staff True
        # evaluate True
        return bool(request.user and request.user.is_staff)

'''
Permissions classes that inherit from 
BasePermission can be combined using the 
bitwise operators & (and), | (or), and ~ (not)

has_permission(self, request, view) and 
has_object_permission(self, request, view, obj)
Methods should return True to allow the request or False to deny it.

However IsAdminUser always returns True from 
has_object_permission(), 
even if a user isn't logged in! 

So by using it we'll give all permissions to everyone.

We can solve this by subclassing IsAdminUser 
and implementing has_object_permission():

in view class define and combine permission classes for view:
class ViewName(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
'''
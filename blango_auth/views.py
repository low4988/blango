from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Note the use of the login_required decorator 
# so that we know we have a logged-in user in that view. 
@login_required
def profile(request):
    return render(request, "blango_auth/profile.html")

# remove registered but unactivated (by email) accounts
@login_required
def rm_unactivated_accounts():
  from datetime import timedelta

  from django.conf import settings
  from django.utils import timezone

  from blango_auth.models import User
  User.objects.filter(
      is_active=False,
      date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
  ).delete()
  # feedback of removed users
  #return render(request, "blango_auth/removed.html")
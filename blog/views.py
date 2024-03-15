from django.shortcuts import render

# Create your views here.

# renders blog index.html, 
# blog/index.html extends base.html
def index(request):
    return render(request, "blog/index.html")
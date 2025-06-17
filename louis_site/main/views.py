from django.shortcuts import render

# Create your views here.
def index(response):
    """
    Render the index page.
    """
    return render(response, "main/index.html")
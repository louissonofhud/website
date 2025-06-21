from django.shortcuts import render

from .forms import BlogPostForm
from .models import BlogPost

# Create your views here.
def index(response):
    """
    Render the index page.
    """
    return render(response, "main/index.html")

def cv(response):
    """
    Render the CV page.
    """
    return render(response, "main/cv.html")

def create_blog_post(response):
    """
    Render the add blog post page.
    """
    if response.method == "POST":
        form = BlogPostForm(response.POST, response.FILES)
        if form.is_valid():
            form.save()
            return render(response, "main/blog_post_created.html", {"form": form}) # Todo: Redirect to the blog post list or detail page after creation

    else:
        form = BlogPostForm()
    return render(response, "main/create_post.html", {"form": form})
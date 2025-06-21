from django.shortcuts import render, redirect
from django.urls import reverse

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
            return redirect(reverse("blog")) 

    else:
        form = BlogPostForm()
    return render(response, "main/create_post.html", {"form": form})

def blog(response):
    """
    Render the blog page with a list of blog posts.
    """
    posts = BlogPost.objects.all().order_by('-created_at')  # Order by creation date, newest first
    if response.method == "POST" and response.POST.get("Create") == "goto":
        return redirect(reverse("add_blog_post"))
    return render(response, "main/blog.html", {"posts": posts})

def blog_post(response, post_id):
    """
    Render a specific blog post.
    """
    try:
        post = BlogPost.objects.get(post_id=post_id)
    except BlogPost.DoesNotExist:
        return render(response, "main/404.html", {"message": "Blog post not found."})

    return render(response, "main/post_detail.html", {"post": post})

def logout(response):
    return render(
        response,
        "main/logout.html",
        {
            "name": "Logout",
        })

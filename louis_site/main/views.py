from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from .forms import BlogPostForm
from .models import BlogPost

# Helper functions

def staff_required(user):
    return user.is_authenticated and user.is_staff

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

@user_passes_test(staff_required, login_url='home')
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
    return render(response, "main/blog_create_post.html", {"form": form})

def blog(response):
    """
    Render the blog page with a list of blog posts.
    """
    if not response.user.is_authenticated:
        posts = BlogPost.objects.filter(private=False).order_by('-created_at')
    else:
        posts = BlogPost.objects.all().order_by('-created_at')
    if response.method == "POST" and response.POST.get("Create") == "goto":
        return redirect(reverse("add_blog_post"))
    return render(response, "main/blog_main.html", {"posts": posts})

def blog_post(response, post_id):
    """
    Render a specific blog post.
    """
    post = BlogPost.objects.get(post_id=post_id)
    if not post:
        return render(response, "main/error.html", {"message": "This blog post not found."})
    elif post.private and not response.user.is_authenticated:
        return render(response, "main/error.html", {"message": "No access to view this post - please log in."})

    comments = post.comments.all()
    top_level_comments = comments.filter(parent=None)
    comment_dict = {}
    for com in top_level_comments:
        comment_dict[com] = [rep for rep in comments.filter(parent=com)]

    return render(response, "main/blog_post_detail.html", {"post": post, "comments": comment_dict})

def error(response):
    """
    Render the error page.
    """
    return render(response, "main/error.html", {"message": "Unknown error, please reach out via the contact form."})

def logout(response):
    return render(
        response,
        "main/logout.html",
        {
            "name": "Logout",
        })

def delete_post(response, issue_id):
    if response.method == "POST":
        if response.POST.get("delete-button") == "delete-confirmed":
            post_to_del = BlogPost.objects.get(id=issue_id)
            post_to_del.delete()
            messages.success(response, "Post deleted")
    return redirect(reverse("blog"))
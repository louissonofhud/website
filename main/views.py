from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.http import FileResponse

import datetime
import os

from .forms import BlogPostForm, CommentForm
from .models import BlogPost, BlogComment

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

    if response.method == "POST":
        if response.POST.get("delete-comment"):
            comment_id = response.POST.get("delete-comment")
            comment_to_delete = BlogComment.objects.get(id=comment_id)
            if comment_to_delete.author != response.user.username:
                messages.error(response, "You can only delete your own comments.")
                return redirect(reverse("post_detail", args=[post.post_id]))
            comment_to_delete.content = "***THIS COMMENT HAS BEEN DELETED***"
            comment_to_delete.deleted = True
            comment_to_delete.save()
            messages.success(response, "Comment deleted successfully.")
            return redirect(reverse("post_detail", args=[post.post_id]))
    
        form = CommentForm(response.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            user = response.user
            author = user.username
            recent_user_comments = BlogComment.objects.filter(
                author=author,
                created_at__gte=timezone.now() - datetime.timedelta(hours=24)
            )
            user_comments = BlogComment.objects.filter(author=author)
            if len(recent_user_comments) > 5:
                messages.error(response, "You have reached the limit of 5 comments in the last 24 hours.")
                return redirect(reverse("post_detail", args=[post.post_id]))
            comm = BlogComment(
                post=post,
                author=author,
                content=content
            )
            comm.save()
            messages.success(response, "Comment added successfully.")
            return redirect(reverse("post_detail", args=[post.post_id]))

    else:
        form = CommentForm()

    return render(response, "main/blog_post_detail.html", {"post": post, "comments": comment_dict, "form": form})

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
            post_to_del_images = post_to_del.all_images
            for image in post_to_del_images:
                if image and hasattr(image, 'path'):
                    try:
                        image.delete(save=False)  # Delete the image file
                    except Exception as e:
                        messages.error(response, f"Error deleting image: {e}")
            post_to_del.delete()
            messages.success(response, "Post deleted")
    return redirect(reverse("blog"))

def download_cv(response):
    filepath = os.path.join("media", "pdf", "Louis Hudson CV.pdf")
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='Louis Hudson CV.pdf')

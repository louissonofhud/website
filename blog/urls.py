from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog, name="blog"),  # List all blog posts
    path("add_post", views.create_blog_post, name="add_blog_post"),  # Create a new blog post
    path("delete_post/<int:issue_id>", views.delete_post, name="delete_post"),  # Delete a blog post
    path("<str:post_id>", views.blog_post, name="post_detail"),  # Display a specific blog post
]
from django.urls import path
from . import views

urlpatterns = [
    path("logout_confirm/", views.logout, name="logout_conf"),
    path("", views.index, name="home"),
    path("cv/", views.cv, name="cv"),
    # path("add_project", views.project_form, name="add_project"), # Create a new project 
    # path("edit_project/<str:project_name>", views.project_form, name="edit_project"), # Edit an existing project
    # path("projects/<str:project_name>", views.display_project, name="show_project"), # Display a specific project
    # path("projects/", views.projects, name="projects"), # List all projects
    path("error/", views.error, name="error"), # Error page
    path("download_cv/", views.download_cv, name="download_cv"), # Download CV
    # path("blog/edit_post/<int:post_id>", views.add_blog_post, name="edit_blog_post"), # Edit an existing blog post
] 
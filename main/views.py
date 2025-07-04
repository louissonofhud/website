from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.http import FileResponse
from django.conf import settings

import datetime
import os

from blog.forms import BlogPostForm, CommentForm
from blog.models import BlogPost, BlogComment

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

def download_cv(response):
    filepath = os.path.join(settings.MEDIA_ROOT, "pdf", "Louis Hudson CV.pdf")
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='Louis Hudson CV.pdf')

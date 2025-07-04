from django.urls import path
from . import views

urlpatterns = [
    path("logout_confirm/", views.logout, name="logout_conf"),
    path("", views.index, name="home"),
    path("cv/", views.cv, name="cv"),
    path("error/", views.error, name="error"), # Error page
    path("download_cv/", views.download_cv, name="download_cv"), # Download CV
] 
from django.db import models

# Create your models here.
class BlogPost(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    private = models.BooleanField(default=False)
    tags = models.CharField(max_length=100, blank=True, help_text="Comma-separated list of tags", null=True) # Maybe I want 
    image1 = models.ImageField(upload_to='blog_images/', blank=True, null=True) # 4 optional images
    image2 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
class BlogPost(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    post_id = models.CharField(max_length=30)  # Unique identifier for each post
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

    def save(self, *args, **kwargs):
        """
        Override save method to ensure post_id is unique.
        """
        if not self.post_id:
            self.post_id = f"self.id"
        self.post_id = self.post_id.replace(" ", "_").lower()
        if BlogPost.objects.filter(post_id=self.post_id).exists():
            self.post_id += "_" + str(self.id)
        instance = super(BlogPost, self).save(*args, **kwargs)
        image = PIL.Image.open(instance.img.path)
        image.save(instance.photo.path, quality=20, optimize=True)
        return instance
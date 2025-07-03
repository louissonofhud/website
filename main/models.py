from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

import PIL
from io import BytesIO

# Create your models here.
class BlogPost(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    post_id = models.CharField(max_length=30, null=True, blank=True)  # Unique identifier for each post
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

        if not self.post_id and len(self.title) < 31:
            self.post_id = self.title

        if self.post_id:
            self.post_id = self.post_id.lower().replace(" ", "_").replace("-", "_")
        else:
            self.post_id = ""
        super().save(*args, **kwargs)  # Call the original save method to get the ID

        if len(BlogPost.objects.filter(post_id=self.post_id)) > 1 or not self.post_id:
            # If the post_id already exists or is empty, append the post ID to make it unique
            self.post_id += str(self.id)

        super().save(update_fields=["post_id"])

        for image_field in ['image1', 'image2', 'image3', 'image4']:
            image = getattr(self, image_field)
            if image and hasattr(image_field, 'path'):
                # Open the image using PIL to ensure it's a valid image
                try:

                    with PIL.Image.open(image.path) as img:
                        if img.mode != "RGB":
                            img = img.convert("RGB")  # Convert to RGB if not already

                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=70, optimize=True)
                    buffer.seek(0)
                
                    new_image = ContentFile(buffer.read(), name=image_field.name.split('/')[-1])
                    setattr(self, field_name, new_image)
                except Exception as e:
                    raise ValidationError(f"Invalid image file for {image_field}: {e}")
        super().save(*args, **kwargs)

    @property
    def all_images(self):
        return [img for img in [self.image1, self.image2, self.image3, self.image4] if img]


class BlogComment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE) # wont add this functionality yet
    author = models.TextField()
    content = models.TextField(max_length=240, help_text="Comment content must be less than 240 characters")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, help_text="Mark comment as deleted without removing it from the database")

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

    def save(self, *args, **kwargs):
        """Override save method to ensure content is not empty and does not exceed 240 characters.
        """
        if len(self.content) > 240:
            raise ValidationError("Comment content must be less than 240 characters.")
        super().save(*args, **kwargs)
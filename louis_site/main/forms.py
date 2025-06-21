from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'content', "post_id",'private', 'image1', 'image2', 'image3', 'image4']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of your blog post'}),
            'post_id': forms.TextInput(attrs={'placeholder': 'Enter the title of your blog post'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'title': 'Headline',
            'content': "Thought content",
            'post_id': "Link ID",
            'private': 'Private post',
            'image1': 'Upload an Image',
            'image2': 'Upload an Image',
            'image3': 'Upload an Image',
            'image4': 'Upload an Image',
        }
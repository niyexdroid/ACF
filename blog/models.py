from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Tour', 'Tour'),
        ('Travel', 'Travel'),
        ('Health', "Health"),
        ('Diet', 'Diet'),
        ('Lifestyle', "Lifestyle"),
    )
    label = models.CharField(max_length=200, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self) -> str:
        return self.label
        
class Post(models.Model):
    title = models.CharField(max_length=1000)
    url_aware_title = models.CharField(max_length=1000, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images', blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts', null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', null=True)
    comment_count = models.IntegerField(null=True)
    

    # timestamps...
    last_modified = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'url_aware_title':self.url_aware_title})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.url_aware_title = '-'.join(self.title.lower().split())
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-last_modified', '-creation_date']
    

# This will track the comments on various events
class Comment(models.Model):
    commentor_name = models.CharField(max_length=150, null=True)
    commentor_image = models.ImageField(default="commentor_images/default.jfif", upload_to='commentor_images', blank=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)

    # likes = models.IntegerField(default=0)
    # disikes = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content}"
    class Meta:
        ordering = ['-creation_date']

class Video(models.Model):
    url = models.CharField(max_length=200, null=True)
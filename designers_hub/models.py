from django.db import models
from django.conf import settings

# Create your models here.

class User_info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_password = models.CharField(max_length=100)
    user_img = models.ImageField(upload_to='user-images', null=True, blank=True)

    def __str__(self):
        return self.user.username


CATEGORY_CHOICES = (
    ('Branding', 'Branding'),
    ('Marketing', 'Marketing'),
    ('Sketch', 'Sketch'),
    ('Photography', 'Photography'),
    ('Creator', 'Creator'),
)

class Post(models.Model):
    author = models.ForeignKey(User_info, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='images')
    description = models.TextField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=14)
    created_at = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.author.user.username}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return f"{self.user.username}"


class NewsLetterEmail(models.Model):
    email = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"
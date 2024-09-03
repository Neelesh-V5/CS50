from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followed_by  = models.PositiveIntegerField(default = 0)
    following = models.PositiveIntegerField(default = 0)

'''
    Each post should include the username of the poster, the post content itself, the date and time at which the post was made, 
    and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).
'''
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE,related_name="poster")
    contents = models.TextField(max_length = 999)
    timestamp = models.DateTimeField(auto_now_add = True)
    edited = models.BooleanField(default = False)
    last_mod = models.DateTimeField(null = True, blank = True)
    likes = models.PositiveIntegerField(default = 0)

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'followed')  
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'follower')  

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete = models.CASCADE)




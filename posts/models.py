from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profiles 
# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True ,validators=[FileExtensionValidator( ['png','jpg','jpeg'])])
    liked = models.ManyToManyField(Profiles,blank=True,related_name = 'likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name= 'posts')
    def __str__(self):
        return str(self.content[:20])
    def num_likes(self):
        return self.liked.all().count()
    def num_comments(self):
        return self.comment_set.all().count()
    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices = LIKE_CHOICES,max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
    

    
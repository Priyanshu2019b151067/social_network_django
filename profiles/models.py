from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .utils import get_random_code
from django.db.models import Q
# Create your models here.



class ProfilesManager(models.Manager):

    def get_all_profiles_to_invite(self,sender):
        profiles = Profiles.objects.all().exclude(user=sender)
        profile = Profiles.objects.get(user = sender)
        qs = Relationship.objects.filter(Q(sender=profile)|Q(receiver = profile))
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        available = [profile for profile in profiles if profile not in accepted]
        return available


    def get_all_profiles(self,me):
        profiles = Profiles.objects.all().exclude(user =me)
        return profiles


class Profiles(models.Model):
    firstname = models.CharField(max_length=200,blank=True)
    lastname =models.CharField(max_length=200,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="nothing here",max_length=300)
    email = models.EmailField(max_length=254,blank=True)
    country = models.CharField(max_length=200,blank=True)
    avatar = models.ImageField(default='man.png',upload_to="profiles/")
    friends = models.ManyToManyField(User, blank=True,related_name ='friends')
    slug = models.SlugField(unique=True,blank=True)
    updated= models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfilesManager()
    

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    def get_absolute_url(self):
        return reverse("profile-detail-view", kwargs={"slug": self.slug})
    
    

    def get_friends(self):
        return self.friends.all()
    def get_friends_no(self):
        return self.friends.all().count()
    def get_posts_no(self):
        return self.posts.all().count()
    def get_all_authors_posts(self):
        return self.posts.all()
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for items in likes:
            if items.value == 'Like':
                total_liked +=1
        return total_liked
    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for items in posts:
            total_liked += items.liked.all().count()
        return total_liked

    
    __initial_firstname = None
    __initial_lastname = None

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__initial_firstname = self.firstname
        self.__initial_lastname = self.lastname
    
    def save(self,*args, **kwargs):
        ex = False
        toslug = self.slug
        if self.firstname != self.__initial_firstname or self.lastname != self.__initial_lastname or self.slug=="":
            if self.firstname and self.lastname:
                toslug = slugify(str(self.firstname)+ "" + str(self.lastname))
                ex= Profiles.objects.filter(slug = toslug).exists()
                while ex: 
                    toslug=slugify(toslug + "" + str(get_random_code()))    
                    ex= Profiles.objects.filter(slug = toslug).exists()
            else:
                toslug=str(self.user)
        self.slug=toslug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted')
)

class RelationshipManager(models.Manager):
    def invatations_received(self,receiver):
        qs = Relationship.objects.filter(receiver = receiver,status = 'send')
        return qs

class Relationship(models.Model):
    sender= models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="receiver")
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated= models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    



from django.db import models
import datetime
from django.contrib.auth.models import User
from django.urls import reverse
import math
from django.utils.translation import gettext as _




# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='user_profile_pics/default3.png', upload_to='user_profile_pics', null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

    

   

# We will need this information from users that want to make a donation
class Donator(models.Model):
    # full_name = models.CharField(_("Donator Full Name"), max_length=150, null=True)
    full_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    picture = models.ImageField(upload_to = 'donator_images', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name}, {self.email}"
    
        



# This will track the various causes for the foundation
class Cause(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to='cause_images')
    target_amount = models.IntegerField()
    reached_amount = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uploaded_causes', null=True)
    

    def percentage(self):
        try:
            return math.floor((self.reached_amount/self.target_amount)*100)
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return f"{self.title}, {self.target_amount}, {self.id}"





# This tracks every donation made for a cause
class Donation(models.Model):
    donator = models.ForeignKey(Donator,on_delete= models.PROTECT, related_name='donations')
    cause  = models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='donations')
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    

    def __str__(self): 
        # return f"{self.donator.full_name}, {self.amount}, {self.id}, {self.time}"
        pass

    
    # to change the ordering, we use a meta class
    class Meta:
        ordering = ['-time']





# This will track the events for the foundation
class Event(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    date = models.DateField()
    time = models.CharField(max_length = 50, null = True)
    venue = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='event_images')
    cause  =  models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='event', blank = True)
    comment_count = models.IntegerField(default = 0)
    # the name for this field should probably be something else other than creator...
    creator = models.ForeignKey(User, related_name='uploaded_events', on_delete=models.PROTECT, null=True)
        
    #optional
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        ordering = ['-date']
    
    def get_absolute_url(self):
        return reverse('main:event-single_view', kwargs={'id':self.id})
    
    def get_absolute_gallery_url(self):
        return reverse('main:event-single-gallery_view', kwargs={'id':self.id})




# This will serve as a means of storing additional pictures for the gallery 
class EventPic(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='pics')
    image = models.ImageField(upload_to='event_images')




# This will track volunteers, or at least people who send the email
class Volunteer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    volunteer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-volunteer_date']
    
    def __str__(self):
        return self.name



class Contactor(models.Model):
    name = models.CharField(max_length=150)
    message = models.TextField()
    email = models.EmailField()
    contact_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-contact_date']
    
    def __str__(self):
        return f"{self.name}, {self.email}"


# Kinda self explanatory...
class NewsLetterMember(models.Model):
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
    

class TeamMember(models.Model):
    name = models.CharField(max_length = 150)
    position  = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'team_member_images')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class meta:
        ordering = ['-date_added']
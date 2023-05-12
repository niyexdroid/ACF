from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Donator)
class DonatorAdmin(admin.ModelAdmin):
    model = Donator
    list_display = ['full_name', 'email']

@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    model = Cause
    list_display = ['title', 'target_amount', 'reached_amount']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    model = Donation
    list_display = ['donator_name', 'amount', 'event_name']
    @admin.display()
    def donator_name(self, obj):
        return obj.donator.full_name
    @admin.display()
    def event_name(self, obj):
        return obj.cause.title

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ['name', 'cause_title', 'date']
    @admin.display()
    def cause_title(self, obj):
        return obj.cause.title

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model= UserProfile
    list_display = ['user_name', 'bio', 'phone']
    @admin.display()
    def user_name(self, obj):
        return obj.user.username

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    model= Volunteer
    list_display = ['name', 'email']

@admin.register(NewsLetterMember)
class NewsLetterMemberAdmin(admin.ModelAdmin):
    model= NewsLetterMember
    list_display = ['email']

admin.site.register(EventPic)

@admin.register(Contactor)
class ContactorAdmin(admin.ModelAdmin):
    model = Contactor
    list_display = ['name', 'email', 'message', 'contact_date']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    model = TeamMember
    list_display = ['name', 'position', 'image', 'date_added'] 
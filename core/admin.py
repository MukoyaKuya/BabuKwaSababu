from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Subscriber, Volunteer, PlatformIssue, NewsArticle, Endorsement, CampaignSettings, CampaignVideo

@admin.register(CampaignSettings)
class CampaignSettingsAdmin(ModelAdmin):
    list_display = ("__str__",)

@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ("email", "first_name", "last_name", "constituency", "ward", "phone_number", "created_at")
    search_fields = ("email", "first_name", "last_name", "constituency", "ward", "phone_number")

@admin.register(Volunteer)
class VolunteerAdmin(ModelAdmin):
    list_display = ("name", "email", "skill", "created_at")
    list_filter = ("skill",)
    search_fields = ("name", "email")

@admin.register(PlatformIssue)
class PlatformIssueAdmin(ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")

@admin.register(NewsArticle)
class NewsArticleAdmin(ModelAdmin):
    list_display = ("headline", "source", "date", "is_featured")
    list_filter = ("source", "is_featured")
    search_fields = ("headline", "source")

@admin.register(Endorsement)
class EndorsementAdmin(ModelAdmin):
    list_display = ("name", "organization", "order")
    list_editable = ("order",)
@admin.register(CampaignVideo)
class CampaignVideoAdmin(ModelAdmin):
    list_display = ("title", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("title", "youtube_id")

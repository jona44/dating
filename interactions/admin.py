from django.contrib import admin
from .models import Like, Match, Block, Report

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('from_profile', 'to_profile', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('from_profile__display_name', 'to_profile__display_name')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('profile1', 'profile2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('profile1__display_name', 'profile2__display_name')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('blocker', 'blocked', 'created_at')
    list_filter = ('created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported', 'reporter', 'reason', 'status', 'created_at')
    list_filter = ('reason', 'status', 'created_at')
    search_fields = ('reported__display_name', 'reporter__display_name', 'description')
    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_as_reviewed.short_description = "Mark selected reports as reviewed"

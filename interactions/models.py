import uuid
from django.db import models
from django.conf import settings


class Like(models.Model):
    from_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="likes_sent")
    to_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="likes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_profile", "to_profile")

    def __str__(self):
        return f"{self.from_profile} → {self.to_profile}"


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile1 = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="matches_as_profile1")
    profile2 = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="matches_as_profile2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile1", "profile2")

    def __str__(self):
        return f"Match: {self.profile1} ↔ {self.profile2}"

    def other_profile(self, profile):
        return self.profile2 if self.profile1 == profile else self.profile1


class Block(models.Model):
    """Track blocked users"""
    blocker = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='blocks_made')
    blocked = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blocker', 'blocked')
        indexes = [
            models.Index(fields=['blocker', 'blocked']),
        ]
    
    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"


class Report(models.Model):
    """User reports for inappropriate behavior"""
    REASON_CHOICES = [
        ('spam', 'Spam or fake account'),
        ('inappropriate', 'Inappropriate content or behavior'),
        ('harassment', 'Harassment or bullying'),
        ('underage', 'Appears to be underage'),
        ('scam', 'Scam or fraud'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('action_taken', 'Action Taken'),
        ('dismissed', 'Dismissed'),
    ]
    
    reporter = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='reports_made')
    reported = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.reporter} reported {self.reported} for {self.reason}"


class Skip(models.Model):
    """Track profiles a user has chosen to pass on in discovery"""
    from_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="skips_sent")
    to_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="skips_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_profile", "to_profile")

    def __str__(self):
        return f"{self.from_profile} skipped {self.to_profile}"


class ProfileView(models.Model):
    """Track when a user views another user's profile"""
    viewer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="views_made")
    viewed = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name="views_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['viewed', '-created_at']),
            models.Index(fields=['viewer', 'viewed']),
        ]

    def __str__(self):
        return f"{self.viewer} viewed {self.viewed} at {self.created_at}"

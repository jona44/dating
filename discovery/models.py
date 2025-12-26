from django.db import models
from accounts.constants import COUNTRY_CHOICES, CITY_CHOICES


class Preference(models.Model):
    """Store user's discovery preferences and search criteria"""
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE, related_name='preferences')
    
    # Age preferences
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=99)
    
    # Gender preferences
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('all', 'All'),
    ]
    interested_in = models.CharField(max_length=10, choices=GENDER_CHOICES, default='all')
    
    # Location preferences
    pref_city = models.CharField(max_length=100, choices=CITY_CHOICES, blank=True, help_text="Preferred city")
    
    # Lifestyle preferences
    pref_max_children = models.IntegerField(null=True, blank=True, help_text="Maximum number of children a partner has")
    pref_nationality = models.CharField(max_length=100, choices=COUNTRY_CHOICES, blank=True, help_text="Preferred nationality")
    
    ETHNICITY_CHOICES = [
        ('any', 'Any'),
        ('white', 'White / Caucasian'),
        ('black', 'Black'),
        ('Shona','Shona'),
        ('Zimbabwean','Zimbabwean'),
        ('ndebele','Ndebele'),
        ('Zulu','Zulu'),
        ('Xhosa','Xhosa'),
        ('Tswana','Tswana'),
        ('pedi','Pedi'),
        ('tsonga','Tsonga'),
        ('swazi','Swazi'),
        ('venda','Venda'),
        ('colored','Colored'),
        ('indian','Indian'),
        
        
    ]
    pref_ethnicity = models.CharField(max_length=30, choices=ETHNICITY_CHOICES, default='any')
    
    # Visibility
    show_me = models.BooleanField(default=True, help_text="Show my profile in discovery")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.profile.display_name}"

from django import forms
from .models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # signal will create Profile
        return user


# Onboarding Step Forms
class OnboardingStep1Form(forms.ModelForm):
    """Basic Information"""
    class Meta:
        model = Profile
        fields = ['display_name', 'birth_date', 'gender', 'city']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'placeholder': 'Your name'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'gender': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
        }


class OnboardingStep2Form(forms.ModelForm):
    """Personal Details"""
    class Meta:
        model = Profile
        fields = ['nationality', 'ethnicity', 'education_level', 'employment_status', 'children_status', 'children_count', 'hobbies', 'height', 'smoking', 'drinking']
        widgets = {
            'nationality': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'ethnicity': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'education_level': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'employment_status': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'children_status': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'x-model': 'children_status'}),
            'children_count': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 0}),
            'hobbies': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'rows': 3, 'placeholder': 'e.g. Reading, hiking, cooking, music...'}),
            'height': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'placeholder': 'Height in cm'}),
            'smoking': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'drinking': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
        }


class OnboardingStep3Form(forms.ModelForm):
    """HIV Journey - All Optional"""
    class Meta:
        model = Profile
        fields = ['diagnosis_year', 'treatment_status', 'disclosure_comfort', 'support_seeking']
        widgets = {
            'diagnosis_year': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'placeholder': 'YYYY', 'min': '1980', 'max': '2024'}),
            'treatment_status': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'disclosure_comfort': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'support_seeking': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-pink-600 focus:ring-pink-500 border rounded'}),
        }


class OnboardingStep4Form(forms.ModelForm):
    """Photos & Bio"""
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'rows': 5, 'placeholder': 'Tell others about yourself, your interests, what you\'re looking for...'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'placeholder': 'General area (optional)'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-pink-500', 'accept': 'image/*'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name", "birth_date", "gender", "city", "nationality", "ethnicity",
            "bio", "profile_picture", "education_level", "employment_status",
            "children_status", "children_count", "hobbies", "height", "smoking", "drinking",
            "diagnosis_year", "treatment_status", "disclosure_comfort", "support_seeking"
        ]

        widgets = {
            "display_name": forms.TextInput(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "placeholder": "Your name"}),
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "gender": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "city": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "nationality": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "ethnicity": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "bio": forms.Textarea(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "rows": 4, "placeholder": "Tell us about yourself..."}),
            "profile_picture": forms.FileInput(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "accept": "image/*"}),
            "education_level": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "employment_status": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "children_status": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "x-model": "children_status"}),
            "children_count": forms.NumberInput(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "min": 0}),
            "hobbies": forms.Textarea(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "rows": 2, "placeholder": "Reading, Music..."}),
            "height": forms.NumberInput(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "placeholder": "cm"}),
            "smoking": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "drinking": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "diagnosis_year": forms.NumberInput(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500", "placeholder": "YYYY"}),
            "treatment_status": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "disclosure_comfort": forms.Select(attrs={"class": "w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500"}),
            "support_seeking": forms.CheckboxInput(attrs={"class": "w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500"}),
        }

        labels = {
            "display_name": "Display Name",
            "birth_date": "Date of Birth",
            "gender": "Gender Identity",
            "support_seeking": "Interested in community support?",
            "disclosure_comfort": "Comfort with disclosing status",
        }


class UserSettingsForm(forms.ModelForm):
    """Form for general account settings"""
    class Meta:
        model = Profile
        fields = ['is_visible']
        labels = {
            'is_visible': 'Profile Visibility (Show me in discovery)',
        }
        widgets = {
            'is_visible': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500'}),
        }

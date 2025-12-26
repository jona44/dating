from django import forms
from .models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['min_age', 'max_age', 'interested_in', 'pref_city', 'pref_max_children', 'pref_nationality', 'pref_ethnicity', 'show_me']
        widgets = {
            'min_age': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 18, 'max': 99}),
            'max_age': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 18, 'max': 99}),
            'interested_in': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'pref_city': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'pref_max_children': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 0, 'placeholder': 'Max children partner has'}),
            'pref_nationality': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'pref_ethnicity': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'show_me': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500'}),
        }
        labels = {
            'min_age': 'Minimum Age',
            'max_age': 'Maximum Age',
            'interested_in': 'I am looking for',
            'pref_city': 'Preferred City',
            'pref_max_children': 'Partner children limit',
            'pref_nationality': 'Preferred Nationality',
            'pref_ethnicity': 'Preferred Ethnicity',
            'show_me': 'Show my profile in discovery',
        }

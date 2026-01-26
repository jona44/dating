from django import forms
from .models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['min_age', 'max_age', 'interested_in', 'pref_nationality', 'pref_city', 'pref_ethnicity', 'pref_max_children', 'show_me']
        widgets = {
            'min_age': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 18, 'max': 99}),
            'max_age': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 18, 'max': 99}),
            'interested_in': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500'}),
            'pref_nationality': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'id': 'id_pref_nationality'}),
            'pref_city': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'id': 'id_pref_city'}),
            'pref_ethnicity': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'id': 'id_pref_ethnicity'}),
            'pref_max_children': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-pink-500', 'min': 0}),
            'show_me': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-pink-600 border-gray-300 rounded focus:ring-pink-500'}),
        }
        labels = {
            'min_age': 'Minimum Age',
            'max_age': 'Maximum Age',
            'interested_in': 'Interested In',
            'pref_nationality': 'Preferred Country',
            'pref_city': 'Preferred City',
            'pref_max_children': 'Max Children partner has',
            'pref_ethnicity': 'Preferred Ethnicity',
            'show_me': 'Show my profile in discovery',
        }

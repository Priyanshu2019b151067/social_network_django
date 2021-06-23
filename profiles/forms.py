from django import forms
from .models import Profiles
class ProfilesModelForm(forms.ModelForm):
    
    class Meta:
        model = Profiles
        fields = ("firstname","lastname","bio","avatar")

    

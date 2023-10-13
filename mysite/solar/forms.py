
from .models import ObjektasReview, Profilis, Objektas
from django import forms
from django.contrib.auth.models import User


class ObjektasReviewForm(forms.ModelForm):
    class Meta:
        model = ObjektasReview
        fields = ['objektas']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']

class DateInput(forms.DateInput):
    input_type = "date"


class UserObjektaiCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Objektas
        fields = ['adresas']

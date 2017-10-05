from django import forms

from Main import models
from .models import CustomData, Post




class SignupForm(forms.Form):
    model = CustomData
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=25)
    user_type = forms.IntegerField()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.custom.type = self.cleaned_data['user_type']
        user.custom.phone = self.cleaned_data['phone']

        if user.custom.type != models.CustomData.REALTOR:
            user.custom.verified = True

        user.save()

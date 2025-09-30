from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Classroom, Enrollment, Test, Question, Answer
from django.contrib.auth.models import User
import datetime

class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields= ('name', 'code', 'desc')
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Classroom Name'}),
        'desc':forms.Textarea(attrs={ 'rows': 5, 'class':'form-control','placeholder':'Description'}),
        'code':forms.TextInput(attrs={'class':'form-control','placeholder':'Unique Code'})
        }

class CreateTestForm(forms.ModelForm):
  class Meta:
    model = Test
    fields=( 'name', 'desc', 'start_time', 'end_time' )
    widgets={
    'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Test Name'}),
    'desc':forms.Textarea(attrs={ 'rows': 5, 'class':'form-control','placeholder':'Description or Instructions'}),
    'start_time': forms.DateTimeInput(attrs={'type':'datetime-local','placeholder':'Assign Test At','class': 'form-control'},format='%Y-%m-%dT%H:%M'),
    'end_time': forms.DateTimeInput(attrs={'type':'datetime-local','placeholder':'Due Time', 'class': 'form-control'},format='%Y-%m-%dT%H:%M'),
    }
    labels={
        'name': 'Test Name',
        'desc': 'Description',
        'start_time': 'Start Time',
        'end_time': 'End Time',
    }


class CreateQnForm(forms.ModelForm):
  class Meta:
    model = Question
    fields=( 'qn_text', 'key', 'max_score')
    widgets={
    'qn_text':forms.Textarea(attrs={ 'rows': 2, 'class':'form-control','placeholder':'Question'}),
    'key':forms.Textarea(attrs={ 'rows': 3, 'class':'form-control','placeholder':'Answer Key'}),
    'max_score':forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder':'Max Score'})
    }

class UserForm(UserChangeForm):
    class Meta:
        model=User
        fields=['email','first_name','username']
        labels={
            'email': 'Email ID',
            'username':'Username',
            'first_name':'Name'
        }
        widgets={
        'email':forms.EmailInput(attrs={'class':'form-control',}),
        'first_name':forms.TextInput(attrs={'class':'form-control',}),
        'username':forms.EmailInput(attrs={'class':'form-control'}),
        }

# class PasswordForm(PasswordChangeForm):
#     fields=['old_password', 'new_password', 'new_password_confirmation']
#     old_password = forms.CharField(required=True, label='Current Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Current Password'}))
#     new_password = forms.CharField(required=True, label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
#     new_password_confirmation = forms.CharField(required=True, label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password, again'}))
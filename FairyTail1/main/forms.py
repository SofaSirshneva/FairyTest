import json
from django import forms
from main.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import DateInput, Select, PasswordInput, CheckboxInput, FileInput

class DateInput(forms.DateInput):
    input_type = 'date'

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i=0
        
        CITY=()
        REGION=()

        """  with open('main/static/main/cities.json', 'r',  encoding="utf8") as f:
            city =  json.load(f)
        with open('main/static/main/region.json', 'r',  encoding="utf8") as f:
            region =  json.load(f) """

        with open('FairyTail1\main\static\main\cities.json', 'r',  encoding="utf8") as f:
            city =  json.load(f)
        with open('FairyTail1\main\static\main\pegion.json', 'r',  encoding="utf8") as f:
            region =  json.load(f)
        
        while i!= 78:
            REGIONS=[i]
            REGIONS.append(region[i]['name'])
            RE=tuple(REGIONS)
            REGION+=RE,
            i=i+1

        i=0

        while i!= 2513:
            CITIES=[i]
            CITIES.append(city[i]['name'])
            CI=tuple(CITIES)
            CITY+=CI,
            i=i+1

        self.fields["first_name"].widget.attrs.update({
            'type' : 'text',
            'class' : 'form-control',
            'id' : 'name',
            'required' : '',
        })
        self.fields["last_name"].widget.attrs.update({
            'type' : 'text',
            'class' : 'form-control',
            'id' : 'surname',
            'required' : '',
        })
        self.fields["username"].widget.attrs.update({
            'type' : 'text',
            'class' : 'form-control',
            'id' : 'login',
            'required' : '',
        })
        self.fields["email"].widget.attrs.update({
            'type' : 'email',
            'class' : 'form-control',
            'id' : 'email',
            'placeholder' : 'you@example.com',
            'required' : '',
        })
        self.fields["number"].widget.attrs.update({
            'type' : 'text',
            'class' : 'form-control mask-phone',
            'id' : 'number',
        })
        """  self.fields["date_of_birth"].widget.attrs.update({
            'input_type' : 'date',
            'class' : 'form-control',
            'id' : 'dateofbirth',
            'required' : '',
        }) """
        self.fields["country"] =  forms.ChoiceField(required=True, choices=REGION, initial='Выбор...',
                                widget=Select({
                                    'class' : 'form-select',
                                }))
        self.fields["city"] =  forms.ChoiceField(required=True, choices=CITY, 
                                widget=Select({
                                    'class' : 'form-select',
                                }))
        self.fields["date_of_birth"] = forms.DateField(required=True,
                           widget=DateInput({
                               'class': 'form-control',
                           }))
        self.fields["password"] = forms.CharField(required=True,
                           widget=PasswordInput({
                               'class': 'form-control',
                           }))
        self.fields["password1"] = forms.CharField(required=False,
                           widget=PasswordInput({
                               'class': 'form-control',
                           }))
        self.fields["password2"] = forms.CharField(required=False,
                           widget=PasswordInput({
                               'class': 'form-control',
                           }))
        self.fields["mailing"] = forms.BooleanField(required=False,
                           widget=CheckboxInput({
                               'class': 'form-check-input',
                               'checked' : 'checked'
                           }))
        """  self.fields["avatar"] = forms.ImageField(required=False,
                           widget=FileInput({
                               'class' : 'loadava',
                               'onchange' : 'loadFile(event)'
                           })) """

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'number', 'date_of_birth', 'country', 'city', 'password', 'mailing')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

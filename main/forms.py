import json
from django import forms
from main.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms.widgets import DateInput, Select, PasswordInput, CheckboxInput, FileInput, TextInput, EmailInput
from django.contrib.auth.password_validation import validate_password

class DateInput(forms.DateInput):
    input_type = 'date'

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        i=0
        REGION=()

        with open('main\static\main\pegion.json', 'r',  encoding="utf8") as f:
            region =  json.load(f)

        """with open('FairyTail1\main\static\main\pegion.json', 'r',  encoding="utf8") as f:
            region =  json.load(f) """
        
        while i!= 78:
            REGIONS=[i]
            REGIONS.append(region[i]['name'])
            RE=tuple(REGIONS)
            REGION+=RE,
            i=i+1

        self.fields["first_name"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
        self.fields["last_name"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
        self.fields["username"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
        self.fields["email"] = forms.EmailField(required=True,
                                widget=EmailInput({
                                    'class' : 'form-control',
                                    'id' : 'email',
                                    'placeholder' : 'you@example.com',
                                    }))
        self.fields["number"] = forms.CharField(required=False,
                                widget=TextInput({
                                    'class' : 'form-control mask-phone',
                                    'id' : 'number',
                                }))
        self.fields["country"] =  forms.ChoiceField(required=True, choices=REGION,
                                widget=Select({
                                    'class' : 'form-select',
                                    'onchange' : 'choicecity(document.getElementById("id_country").value)',
                                    'id': 'id_country'
                                }))
        self.fields["city"] =  forms.CharField(required=True,
                                widget=Select({
                                    'class' : 'form-select',
                                    'id' : 'id_city'
                                }))
        self.fields["date_of_birth"] = forms.DateField(required=True,
                           widget=DateInput({
                               'class': 'form-control',
                               'min' : "1900-01-01",
                               'max' : "2016-12-31"
                           }))
        self.fields["password1"] = forms.CharField(required=True,
                           widget=PasswordInput({
                               'class': 'form-control',
                           }))
        self.fields["password2"] = forms.CharField(required=True,
                           widget=PasswordInput({
                               'class': 'form-control',
                           }))
        self.fields["mailing"] = forms.BooleanField(required=False,
                           widget=CheckboxInput({
                               'checked' : 'checked'
                           }))
        self.fields["avatar"] = forms.ImageField(required=False,
                           widget=FileInput({
                               'class' : 'loadava',
                               'onchange' : 'loadFile(event)'
                           }))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'number', 'date_of_birth', 'country', 'city', 'password1', 'password2', 'mailing', 'avatar')

    def clean_password(self):
        password = self.cleaned_data['password1']
        validate_password(password)
        return password

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_number(self):
        number = self.cleaned_data['number']
        if CustomUser.objects.filter(number=number).exists():
            raise forms.ValidationError('Пользователь с таким номером уже существует')
        return number

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class LoginUserForm(AuthenticationForm):
       
        username = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                    'id' : 'floatingInput'
                                }))

        password = forms.CharField(required=True,
                           widget=PasswordInput({
                               'class': 'form-control',
                               'id' : 'floatingPassword'
                           }))


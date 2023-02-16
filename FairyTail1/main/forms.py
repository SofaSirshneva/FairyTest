import json
from django import forms
from main.models import CustomUser, Tests, Questions, Answers
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms.widgets import DateInput, Select, PasswordInput, CheckboxInput, FileInput, TextInput, EmailInput, RadioSelect, SelectMultiple
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from main.multiform import MultiModelForm

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
                               'class': 'form-check-input',
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

class CreateTestForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PRIVATE =[
            ('0','Открытый'),
            ('1','Закрытый')
        ]

        self.fields["name"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))

        self.fields["private"] = forms.ChoiceField(required=True, choices=PRIVATE,
                                widget=RadioSelect({
                                    'onchange' : 'defprivate()',
                                }))

        self.fields["password"] = forms.CharField(required=False,
                                widget=TextInput({
                                    'class' : 'form-control',
                                    'id' : 'test_password'
                                }))
        self.fields["time_control"] = forms.IntegerField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
        self.fields["categories"] = forms.CharField(required=False,
                                widget=SelectMultiple({
                                    'class' : 'form-control',
                                }))
    
    class Meta:
        model = Tests
        fields = ('name', 'private', 'password', 'time_control', 'categories')

    categories2 = forms.CharField(required=False,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))

class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["text"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
    
    class Meta:
        model = Questions
        fields = ('text', )

class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["text_content"] = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))

    class Meta:
        model = Answers
        fields = ('text_content', 'correctness')

class AddQuestionForm(MultiModelForm):
    form_classes = {
        'question': QuestionForm,
        'answers': AnswerForm,
    }

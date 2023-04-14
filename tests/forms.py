from django import forms
from .models import Tests, Questions, Answers, Categories
from django.forms.widgets import TextInput, RadioSelect, SelectMultiple, Textarea, PasswordInput, CheckboxSelectMultiple

class TestForm(forms.ModelForm):
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
                                widget=PasswordInput({
                                    'class' : 'form-control',
                                    'id' : 'test_password'
                                }))
        self.fields["time_control"] = forms.IntegerField(required=True, 
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))
    class Meta:
        model = Tests
        fields = ('name', 'private', 'password', 'time_control')

    categories2 = forms.CharField(required=False,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))

    categories = Categories.objects.all().order_by('name')
    CATEGORY = ()

    for category in categories:
        CATEGORIES=[category.id]
        CATEGORIES.append(category.name.capitalize)
        CAT=tuple(CATEGORIES)
        CATEGORY+=CAT,

    categories1 = forms.MultipleChoiceField(required=False, choices = CATEGORY,
                                widget=SelectMultiple({
                                    'class' : 'form-control',
                                }))
    

class QuestionForm(forms.ModelForm):
     text = forms.CharField(required=True,
                                widget=Textarea({
                                    'class' : 'form-control',
                                    'rows' : 5,
                                }))
     class Meta:
        model = Questions
        fields = ('text',)

class AnswerForm(forms.ModelForm):
    text_content = forms.CharField(required=True,
                                widget=TextInput({
                                    'class' : 'form-control',
                                }))

    class Meta:
        model = Answers
        fields = ('text_content', 'correctness')

class TestPassForm(forms.Form):
     
     def __init__(self, question,*args,**kwargs):
        super().__init__(*args,**kwargs)
        ANSWER=()
        for answer in question.answers_set.all():
            ANSWERS=[answer.id]
            ANSWERS.append(answer.text_content)
            AN=tuple(ANSWERS)
            ANSWER+=AN,

        self.fields['radio_answer'] = forms.ChoiceField(choices=ANSWER, required=False,  widget=RadioSelect({
                                    'class' : 'mr answers'
                                    }))
        self.fields['checkbox_answer'] = forms.MultipleChoiceField(choices=ANSWER, required=False, widget=CheckboxSelectMultiple({
                                    'class' : 'mr answers'
                                    }))

     string_answer = forms.CharField(required=False,
                                     widget=TextInput({
                                        'class' : 'form-control inputanswer',
                                     }))
     
class FeedbackForm(forms.Form):
    NUMBER_OF_STARS=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    star = forms.ChoiceField(required=False, choices=NUMBER_OF_STARS, widget=RadioSelect)
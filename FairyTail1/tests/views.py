from django.forms import modelformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .forms import TestForm, QuestionForm, AnswerForm
from django.shortcuts import redirect
from pytils.translit import slugify
from .models import Questions, Tests, Answers, Categories
from django.db.models import Max

class TestCreatePage(CreateView):
    form_class = TestForm
    template_name = "tests/create_test.html"

    def post(self, request):

        if request.method == 'POST':
            form = TestForm(request.POST or None)

            if form.is_valid():
                test = form.save(commit=False)
                test.author = request.user

                try:
                    test.slug = slugify(test.name)
                except:
                    slug_str = test.name + '_' + test.author
                    test.slug = slugify(slug_str)
                
                test.save()

                if form.cleaned_data['categories2']:
                    cat_list = form.cleaned_data['categories2'].split(",")

                    for category in cat_list:
                        category_new = category.lower()

                        try:
                            cat=Categories.objects.get(name=category_new)
                        except:
                            cat = None

                        if not cat:
                            newCat = Categories.objects.create(name=category_new)
                            test.categories.add(newCat)
                        else:
                            test.categories.add(cat)

                        test.save()

                if form.cleaned_data['categories1']:
                    cat_list = form.cleaned_data['categories1']

                    for category in cat_list:
                        try:
                            cat=Categories.objects.get(name=category)
                            test.categories.add(cat)
                            test.save()
                        except:
                            pass

                return redirect(reverse('addquestion', kwargs={'test_slug': test.slug, 'que_num': 0}))
            else:
                return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание теста'
        return context

def add_question(request, test_slug, que_num):

    form1 = QuestionForm(request.POST)
    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, extra=1, max_num=7)
    qs = Questions.objects.none()
    formset = AnswersFormset(request.POST or None, queryset=qs)
    que_num+=1

    if all([form1.is_valid(), formset.is_valid()]):

        question = form1.save(commit=False)
        test = Tests.objects.get(slug = test_slug)
        question.test = test
        question.number = que_num
        correct = False

        for form in formset:
            answer = form.save(commit=False)

            if answer.correctness:
                correct = True
                break
            else:
                pass

        if not correct:

            context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max,
                'errormessage': 'Не отмечен ни один правильный ответ'
            }

            return render(request, 'tests/add_question.html', context)

        question.save()

        for form in formset:
            answer = form.save(commit=False)
            answer.question = question
            answer.save()

        test = Tests.objects.get(slug = test_slug)
        questions = Questions.objects.filter(test=test.pk)
        max = questions.aggregate(Max('number'))

        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max['number__max'],
                'message': 'Вопрос сохранен'
            }

        return render(request, 'tests/add_question.html', context)    
    else:
        test = Tests.objects.get(slug = test_slug)
        questions = Questions.objects.filter(test=test.pk)

        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max,
            }  

        return render(request, 'tests/add_question.html', context)

def update_question(request, tslug, qnum, max):

    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, max_num=7, extra=0)
    test = Tests.objects.get(slug = tslug)
    questions = Questions.objects.filter(test=test.pk)
    question = questions.get(number=qnum)
    qs = Answers.objects.filter(question=question.pk)
    formset = AnswersFormset(request.POST or None, queryset=qs)
    form1 = QuestionForm(request.POST or None, initial={'text': question.text})

    if all([form1.is_valid(), formset.is_valid()]):

        question.text = form1.cleaned_data['text']
        question.save(update_fields=["text"])
        correct = False

        for form in formset:
            answer = form.save(commit=False)
            if answer.correctness:
                correct = True
                break
            else:
                pass

        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': qnum,
                'que_slug': tslug,
                'max': max,
            }

        if not correct:
            return render(request, 'tests/add_question.html', context, {'errormessage': 'Не выбран ни один правильный ответ'})

        for form in formset:
            answer = form.save(commit=False)
            answer.question = question

            if answer.text_content:
                answer.save()

        return render(request, 'tests/add_question.html', context, {'message':'Вопрос сохранен'})
    else:
        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': qnum,
                'que_slug': tslug,
                'max': max,
            }

        return render(request, 'tests/add_question.html', context)

class ProfilePage(ListView):
    template_name='tests/profile.html'
    model = Tests

    def get_queryset(self):
        return Tests.objects.filter(author_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш аккаунт'
        return context





    

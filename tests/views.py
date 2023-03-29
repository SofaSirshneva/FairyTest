import json
from django.forms import modelformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView
from .forms import TestForm, QuestionForm, AnswerForm, TestPassForm
from django.shortcuts import redirect
from pytils.translit import slugify
from .models import Questions, Tests, Answers, Categories, Question_results, Test_results
from django.db.models import Max
from django.db.models.functions import Substr, Upper

class MainPage(ListView):
    template_name='tests/main.html'
    model = Tests

    def get_queryset(self):
        return Tests.objects.order_by('-rating')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context
    
class ProfilePage(ListView):
    template_name='tests/profile.html'
    model = Tests

    def get_queryset(self):
        return Tests.objects.filter(author_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'
        return context

class TestUpdatePage(UpdateView):
    model = Tests
    form_class = TestForm
    template_name = 'tests/create_test.html'

    def form_valid(self, form):
        add_categories(form, self.object)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование теста'
        return context

    def get_success_url(self):
        questions = Questions.objects.filter(test=self.object.pk)
        max = questions.aggregate(Max('number'))
        if  max['number__max']:
            return reverse('updatequestion', kwargs={'test_slug': self.object.slug, 'que_num': 1, 'max': max['number__max']})
        else:
            return reverse('updatequestion', kwargs={'test_slug': self.object.slug, 'que_num': 1, 'max': 1})

class CategoriesPage(ListView):
    template_name= 'tests/categories.html'
    model = Categories

    def get_queryset(self):
        return Categories.objects.order_by('name').annotate(first_letter=Upper(Substr('name', 1, 1)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context
    
class CategoryPage(ListView):
    model = Tests
    template_name = 'tests/category.html'

    def get_queryset(self):
        return Tests.objects.filter(categories=Categories.objects.get(name=self.kwargs['name'])).order_by('-rating')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['name']
        return context
    
class TestInfoPage(DetailView):
    model = Tests
    template_name = 'tests/test_info.html'

    def get_object(self):
        return Tests.objects.get(name=self.kwargs['name'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['name']
        try:
            info = Test_results.objects.filter(user = self.request.user).filter(test=self.object)
        except:
            info = None
        context['flag'] = info
        return context
    
class TestPassPage(DetailView):
    model = Questions
    form_class = TestPassForm
    template_name = 'tests/passing_test.html'

    def get_object(self):
        return Questions.objects.filter(test=Tests.objects.get(slug=self.kwargs['slug'])).get(number=self.kwargs['number'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прохождение теста'
        context['slug'] = self.kwargs['slug']
        context['previous_number'] = self.kwargs['number']-1

        try:
            next_question = Questions.objects.filter(test=Tests.objects.get(slug=self.kwargs['slug'])).get(number=self.kwargs['number']+1)
        except:
            next_question = None
        context['next_number'] = next_question

        result, created = Question_results.objects.get_or_create(user = self.request.user, question = self.object)

        initial_dict = {
            'string_answer': result.answer,
            'radio_answer': result.answer,
        }

        context['checkbox_answer'] = json.dumps(result.answer)
        context['form'] = TestPassForm(question=self.object, initial = initial_dict)

        return context
    
    def post(self, request, slug, number):
        object = Questions.objects.filter(test=Tests.objects.get(slug=self.kwargs['slug'])).get(number=self.kwargs['number'])
        result, created = Question_results.objects.get_or_create(user = request.user, question = object)
        form = TestPassForm(object, request.POST)

        if form.is_valid():
            if object.type == 0:
                result.answer = form.cleaned_data['string_answer']

            elif object.type == 1:
                result.answer = form.cleaned_data['radio_answer']

            else:
                result.answer = form.cleaned_data['checkbox_answer']

            result.save()

        if 'previous' in request.POST:
            number-=1
            return redirect(reverse('testpassing', kwargs={'slug': slug, 'number': number}))
        
        elif 'next' in request.POST:
            number+=1
            return redirect(reverse('testpassing', kwargs={'slug': slug, 'number': number}))
        
        elif 'send' in request.POST:
            return redirect(reverse('testresult', kwargs={'slug': slug}))
        
class TestResultPage(TemplateView):
    template_name = 'tests/test_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты теста'
        context['slug'] = self.kwargs['slug']
        context['result'] = test_result(self.request, self.kwargs['slug'])
        return context
    

def test_result(request, slug):
    result = 0
    test = Tests.objects.get(slug=slug)
    questions = Questions.objects.filter(test=test)
    for question in questions:
        answers = Answers.objects.filter(question=question)
        try:
            user_answer = Question_results.objects.get(question=question).answer
            if question.type == 2:
                correct = []
                for answer in answers:
                    if answer.correctness == True:
                        correct.append(str(answer.id))
            elif question.type == 0:
                for answer in answers:
                    if answer.correctness == True:
                        correct = answer.text_content
            else:
                for answer in answers:
                    if answer.correctness == True:
                        correct = answer.id

            if user_answer == str(correct):
                result+=1
        except:
            pass

    Question_results.objects.filter(user=request.user).delete()
    updated, created = Test_results.objects.update_or_create(user=request.user, test=test)
    updated.result = result
    updated.save()
    if(created):
        test.number_of_passes+=1
        test.average_result = round((test.average_result + result) / test.number_of_passes, 3)
        test.save()

    return result

def add_categories(form, test):
    if form.cleaned_data['categories2']:
        cat_list = form.cleaned_data['categories2'].split(",")

        for category in cat_list:
            category_new = category.lower().lstrip(' ')

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
                cat=Categories.objects.get(id=category)
                test.categories.add(cat)
                test.save()
            except:
                test.save()

def check_answers(question, formset):
    correct = False

    for form in formset:
        answer = form.save(commit=False)

        if answer.correctness:
            correct = True
            break
        else:
            pass

    if not correct:
        return False
    
    number_of_correct = 0
    number_of_answers = 0

    for form in formset:
        answer = form.save(commit=False)
        answer.question = question

        if answer.correctness:
            number_of_correct+=1
        number_of_answers+=1

        answer.save()

    if number_of_answers==1:
        question.type = 0
    elif number_of_correct==1:
        question.type = 1
    else:
        question.type = 2

    question.save()
    return True

class TestCreatePage(CreateView):
    form_class = TestForm
    template_name = "tests/create_test.html"

    def post(self, request):
        form = TestForm(request.POST or None)

        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user

            slug_str = test.name + '_' + test.author.username
            test.slug = slugify(slug_str)

            test.save()
                
            add_categories(form, test)

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
        question.save()

        test = Tests.objects.get(slug = test_slug)
        questions = Questions.objects.filter(test=test.pk)
        max = questions.aggregate(Max('number'))

        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max['number__max']
            }

        if not check_answers(question, formset):
            context['errormessage'] = 'Не отмечен ни один правильный ответ'
            question.delete()
            return render(request, 'tests/add_question.html', context)    
        else:
            context['message'] = 'Вопрос сохранен'
            return render(request, 'tests/add_question.html', context)    
        
    else:
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
            }  

        return render(request, 'tests/add_question.html', context)

def update_question(request, test_slug, que_num, max):

    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, max_num=7, extra=0)
    test = Tests.objects.get(slug = test_slug)
    questions = Questions.objects.filter(test=test.pk)
    question = questions.get(number=que_num)
    qs = Answers.objects.filter(question=question.pk)
    formset = AnswersFormset(request.POST or None, queryset=qs)
    form1 = QuestionForm(request.POST or None, initial={'text': question.text})

    if all([form1.is_valid(), formset.is_valid()]):

        question.text = form1.cleaned_data['text']
        question.save(update_fields=["text"])

        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max['number__max']
            }

        if not check_answers(question, formset):
            context['errormessage'] = 'Не отмечен ни один правильный ответ'
            question.delete()
            return render(request, 'tests/add_question.html', context)    
        else:
            context['message'] = 'Вопрос сохранен'
            return render(request, 'tests/add_question.html', context)    
        
    else:
        context = {
                'title': 'Создание теста',
                'form': form1,
                'formset': formset,
                'que_num': que_num,
                'que_slug': test_slug,
                'max': max,
            }

        return render(request, 'tests/add_question.html', context)


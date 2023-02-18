from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import TestForm, QuestionForm, AnswerForm
from django.shortcuts import redirect
from pytils.translit import slugify
from .models import Questions, Tests, Answers
from django import forms

class TestCreatePage(CreateView):
    form_class = TestForm
    template_name = "tests/create_test.html"

    def post(self, request):
        if request.method == 'POST':
            form = TestForm(request.POST)
            if form.is_valid():
                test = form.save(commit=False)
                test.author = request.user
                test.slug = slugify(test.name)
                test.save()
                return redirect(reverse('addquestion', kwargs={'que_slug': test.slug, 'que_num': '1'}))
            else:
                return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание теста'
        return context

def add_question(request, que_slug, que_num, id=None):
    form1 = QuestionForm(request.POST)
    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, extra=1, max_num=7)
    qs = Questions.objects.none()
    formset = AnswersFormset(request.POST or None, queryset=qs)
    if all([form1.is_valid(), formset.is_valid()]):
        question = form1.save(commit=False)
        test = Tests.objects.get(slug = que_slug)
        question.test = test
        question.save()
        for form in formset:
            answer = form.save(commit=False)
            if answer.correctness:
                break
            else:
                return render(request, 'tests/add_question.html', {'form': form1, 'que_num': que_num, 'formset': formset, 'message': 'Не отмечен ни один правильный ответ'})
        for form in formset:
            answer.question = question
            answer.save()
        que_num+=1
        return redirect(reverse('addquestion', kwargs={'que_slug': test.slug, 'que_num': que_num}))
    else:
        return render(request, 'tests/add_question.html', {'form': form1, 'que_num': que_num, 'formset': formset})

""" class QuestionAddPage(CreateView):
    form = QuestionForm
    form_2 = AnswerForm
    template_name = "tests/add_question.html"

    def post(self, request):
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            form_2 = AnswerForm(request.POST)
            if all([form.is_valid(), form_2.is_valid()]):
                question = form.save(commit=False)
                answer = form_2.save(commit=False)
                question.test = request.test
                question.save()
                answer.question = question
                answer.save()
                return redirect('main')
            else:
                return render(request, self.template_name, {'form': form}) """


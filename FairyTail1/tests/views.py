from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import TestForm, QuestionForm, AnswerForm
from django.shortcuts import redirect
from pytils.translit import slugify
from .models import Questions, Tests, Answers
from django.db.models import Max

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
                return redirect(reverse('addquestion', kwargs={'que_slug': test.slug, 'que_num': 0, 'max': 0}))
            else:
                return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание теста'
        return context

def add_question(request, que_slug, que_num, max):
    form1 = QuestionForm(request.POST)
    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, extra=1, max_num=7)
    qs = Questions.objects.none()
    formset = AnswersFormset(request.POST or None, queryset=qs)
    que_num+=1
    if all([form1.is_valid(), formset.is_valid()]):
        question = form1.save(commit=False)
        test = Tests.objects.get(slug = que_slug)
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
            return render(request, 'tests/add_question.html', {'form': form1, 'que_num': que_num, 'que_slug':  que_slug,
             'formset': formset, 'message': 'Не отмечен ни один правильный ответ'})
        question.save()
        for form in formset:
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
        test = Tests.objects.get(slug = que_slug)
        questions = Questions.objects.filter(test=test.pk)
        max = questions.aggregate(Max('number'))
        return render(request, 'tests/add_question.html', {'form': form1, 'que_num': que_num, 'formset': formset, 'que_slug': que_slug,
         'max': max['number__max'], 'message' :'Вопрос сохранен'})    
    else:
        test = Tests.objects.get(slug = que_slug)
        questions = Questions.objects.filter(test=test.pk)
        max = questions.aggregate(Max('number'))
        return render(request, 'tests/add_question.html', {'form': form1, 'que_num': que_num, 'formset': formset, 'que_slug': que_slug,
         'max': max['number__max']})

def update_question(request, qslug, qnum, max):
    AnswersFormset = modelformset_factory(Answers, form = AnswerForm, max_num=7, extra=0)
    test = Tests.objects.get(slug = qslug)
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
        if not correct:
            return render(request, 'tests/add_question.html', {'form': form1, 'que_num': qnum,
             'que_slug':  qslug, 'formset': formset, 'errormessage': 'Не отмечен ни один правильный ответ'})
        for form in formset:
            answer = form.save(commit=False)
            answer.question = question
            if answer.text_content:
                answer.save()
        max = questions.aggregate(Max('number'))
        return render(request, 'tests/add_question.html', {'form': form1, 'que_num': qnum, 'que_slug':  qslug,
         'formset': formset, 'max': max['number__max'], 'message':'Вопрос сохранен'})
    else:
        max = questions.aggregate(Max('number'))
        return render(request, 'tests/add_question.html', {'form': form1, 'que_num': qnum, 'formset': formset,
         'que_slug': qslug, 'max': max['number__max']})



    

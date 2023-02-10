from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from main.forms import RegisterForm
from django.views.generic.edit import CreateView
from django.shortcuts import redirect

class MainPage(TemplateView):
    template_name='main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

class Error404Page(TemplateView):
    template_name='main/error404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ошибка'
        return context

class Registration(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('enter')
    template_name = "main/registration.html"

    def post(self, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #form.save()
                return redirect('enter')
            else:
                return render(request, self.template_name, {'form': form})

    """ def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return(redirect('enter'))
        else:
            return render(request, self.template_name, {'form' : form})
 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

""" def update_profile(request):
    if request.method == 'POST':
        user_form = Standard(request.POST, instance=request.user)
        profile_form = RegisterForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('enter')
        else:
            return()
            
    else:
        user_form = Standard(instance=request.user)
        profile_form = RegisterForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
 """
class EnterPage(TemplateView):
    template_name='main/enter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

#Svin

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from main.forms import RegisterForm, LoginUserForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from .tokens import account_activation_token 
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.mail import EmailMessage

class Error404Page(TemplateView):
    template_name='main/error404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ошибка'
        return context

class SuccessPage(TemplateView):
    template_name='main/successful_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Успешная регистрация'
        return context

class Registration(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = "main/registration.html"

    def post(self, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request) 
                message = { 
                    'user': user, 
                    'domain': current_site.domain, 
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                    'token':account_activation_token.make_token(user), 
                }
                to_email = form.cleaned_data.get('email')
                ms = get_template('main/mail_text.html').render(context=message)
                msg = EmailMessage('Активация аккаунта', ms, to=[to_email])
                msg.content_subtype = 'html'
                msg.send()
                return redirect('login')
            else:
                return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        t = get_template('main/successful_confirm.html')
        c = {'is_active': True}
        return HttpResponse(t.render(c, request))
    else: 
        return redirect('registration')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "main/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context
    
    def get_success_url(self):
        return reverse_lazy('main')

def logoutUser(request):
    logout(request)
    return redirect('login')

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

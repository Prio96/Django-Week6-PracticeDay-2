from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.views import View
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
# Create your views here.

class UserRegistrationView(FormView):
    template_name='accounts/user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('Register')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        user=form.save()
        login(self.request,user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('Home')
    

class UserLogoutView(LogoutView):#Problem
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        
        return reverse_lazy('Home')

@method_decorator(login_required,name='dispatch')    
class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})

@login_required
def ChangeUserPassword(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            print("Form is valid")
            messages.success(request,"Password Changed Successfully")
            form.save()
            update_session_auth_hash(request,request.user)
            subject="Password Change"
            message=render_to_string("accounts/change_passemail.html",{
                'user':request.user,
            })
            send_email=EmailMultiAlternatives(subject, '', to=[request.user.email])
            send_email.attach_alternative(message,"text/html")
            send_email.send()
            return redirect("Home")
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,"accounts/change_pass.html",{'form':form})
    

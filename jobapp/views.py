from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,UpdateView,ListView,DetailView
from jobapp.forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

# Create your views here.

class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name="register.html"
    success_url=reverse_lazy("login")

    def form_valid(self,form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)
        
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    
class SignInView(FormView):
    model=User
    template_name="login.html"
    form_class=LoginForm
    
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"faild to login")
        return render(request,self.template_name,{"form":form})
    
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=User
    context_object_name="posts"
    success_url=reverse_lazy("index")
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("register")
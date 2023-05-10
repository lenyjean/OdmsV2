from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def login_page(request):
    template_name = 'authentication/login.html'
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        employee_no = request.POST.get('employee_no')
        password = request.POST.get('password')
        print(employee_no, password)
        user = authenticate(request, employee_no=employee_no, password=password)
    
        # print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("homepage")
           
        else:
            messages.error(request, "Invalid employee no. or password")           
    context = {
        "form": form
    }
    return render(request, template_name, context)

def logout_page(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login')
def homepage(request):
    template_name = 'homepage.html'
    context = {
        "home_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)
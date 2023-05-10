from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import uuid

def_uuid = uuid.uuid4()
gen_uuid = str(uuid.uuid4())[:8]

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

def outgoing_docs(request):
    template_name = 'outgoing_docs/outgoing.html'
    document = OutgoingDocs.objects.all().order_by('-date_created')
    context = {
        "document": document
    }
    return render(request, template_name, context)

def add_outgoing(request):
    template_name = 'outgoing_docs/add_outgoing.html'
    form = OutgoingDocsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.tracking_no = gen_uuid
        obj.save()
        return redirect('outgoing-list')
    context = {
        "form": form
    }
    return render(request, template_name, context)

def view_outgoing(request, pk):
    template_name = 'outgoing_docs/view_outgoing.html'
    document = OutgoingDocs.objects.filter(id=pk)
    context = {
        "document": document
    }
    return render(request, template_name, context)

def incoming_docs(request):
    template_name = 'incoming_docs/incoming.html'
    inc_document = IncomingDocs.objects.all().order_by('-date_created')
    context = {
        "document": inc_document
    }
    return render(request, template_name, context)


def category(request):
    template_name = 'category/category_list.html'
    category = Category.objects.all()
    context = {
        "category": category
    }
    return render(request, template_name, context)

def add_category(request):
    template_name = 'category/add_category.html'
    form = CategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    context = {
        "form": form
    }
    return render(request, template_name, context)

def department(request):
    template_name = 'department/department_list.html'
    office = Department.objects.all()
    context = {
        "office": office
    }
    return render(request, template_name, context)

def add_department(request):
    template_name = 'department/add_department.html'
    form = DepartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('department-list')
    context = {
        "form": form
    }
    return render(request, template_name, context)
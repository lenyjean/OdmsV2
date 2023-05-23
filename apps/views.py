from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
import shortuuid

import uuid

def_uuid = uuid.uuid4()
gen_uuid = str(uuid.uuid4())[:8]


def create_tracking(office, status, action, comment, docs):
    Tracking.objects.create(
        office = office,
        status=status,
        action = action,
        comment = comment,
        docs_id=docs
    )

#functions for LOGIN
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
            return redirect("homepage")   
        else:
            messages.error(request, "Invalid employee no. or password")           
    context = {
        "form": form
    }
    return render(request, template_name, context)

#functions for LOGOUT
def logout_page(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("/")

#functions for HOMEPAGE
@login_required(login_url='/login')
def homepage(request):
    template_name = 'homepage.html'
    context = {
        "home_state": "color: #6366f1, font-weight: bold",
    }
    return render(request, template_name, context)

#CATEGORY
#functions for DOCUMENT TYPE/CATEGORY
def category(request):
    template_name = 'category/category_list.html'
    category = Category.objects.all().order_by('-created_at')
    paginator = Paginator(category, 10)
    page_number = request.GET.get('page')
    category = paginator.get_page(page_number)
    context = {
        "category": category,
        "category_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
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

#functions for DEPARTMENT
def department(request):
    template_name = 'department/department_list.html'
    office = Department.objects.all().order_by('-created_at')
    paginator = Paginator(office, 10)
    page_number = request.GET.get('page')
    office = paginator.get_page(page_number)
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

#DOCUMENTS
#functions for OUTGOING DOCUMENTS
def outgoing_docs(request):
    template_name = 'outgoing_docs/outgoing.html'
    document = OutgoingDocs.objects.filter(Q(user__department = request.user.department)).order_by('-date_created')
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    context = {
        "document": document,
    }
    return render(request, template_name, context)

def add_outgoing(request):
    template_name = 'outgoing_docs/add_outgoing.html'
    form = OutgoingDocsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.tracking_no = shortuuid.uuid()[:8] 
        obj.user = request.user
        obj.save()
        create_tracking(office=obj.forwarded_to, status=obj.status, action="", comment="", docs=obj.id)
        Notifications.objects.create(department = obj.forwarded_to, link=f"/outgoing-documents/view/{obj.id}", created_by=request.user, 
                                      message = f"{request.user.first_name} {request.user.last_name} sent you a file",)
        return redirect('outgoing-list')
    context = {
        "form": form
    }
    return render(request, template_name, context)

def view_outgoing(request, pk):
    template_name = 'outgoing_docs/view_outgoing.html'
    document = OutgoingDocs.objects.filter(id=pk)
    Notifications.objects.filter(link=f"/outgoing-documents/view/{pk}").update(is_read=True)
    context = {
        "document": document
    }
    return render(request, template_name, context)

#functions for INCOMING DOCUMENTS
@login_required(login_url='/login')
def release_docs(request, pk):
    template_name = 'incoming_docs/release.html'
    document = get_object_or_404(OutgoingDocs, id=pk)
    list_docs = OutgoingDocs.objects.filter(id=pk)
    form = ReleaseForm(request.POST or None, instance=document)
    actions = request.POST.get('doc_actions')
    if request.method == 'POST':
        obj = form.save(commit=False)
        if actions == 'Pending':
            obj.status = 'Pending'
        elif actions in ['Disapproved', 'No Action']:
            obj.status = 'Denied'
        elif actions in ['Approved', 'Signed', 'Endorsed']:
            obj.status = 'Forwarded'
        obj.save()
        create_tracking(office=obj.forwarded_to, status=obj.status, action=actions, comment="", docs=obj.id)
        Notifications.objects.create(department = obj.forwarded_to, link=f"/outgoing-documents/view/{obj.id}", created_by=request.user, 
                                      message = f"{request.user.first_name} {request.user.last_name} sent you a file",)
        return redirect('outgoing-list')
    context = {
        "form": form,
        "list_docs": list_docs
    }
    return render(request, template_name, context)

#functions for USER ACCOUNTS
@login_required(login_url='/login')
def account(request):
    template_name = 'accounts/account_list.html'
    account = User.objects.all().order_by('-date_joined')
    paginator = Paginator(account, 10)
    page_number = request.GET.get('page')
    account = paginator.get_page(page_number)
    context = {
        "account": account,
        "account_state": "background-color: rgba(212, 210, 210, 1);  color: #fff;",
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def add_account(request):
    template_name = 'accounts/add_account.html'
    form = UserForm(request.POST or None, request.FILES or None)
    department = request.POST.get("department")
    department_name = Department.objects.filter(id=department).first()
    if request.method == 'POST':
        if form.is_valid():
            user_account = form.save(commit=False)
            user_type = request.POST['user_type']
            print(request.POST['user_type'])
            if user_type == "Admin":
                user_account.is_admin = True
            elif user_type == "Employee":
                user_account.is_employee = True
            password = form.cleaned_data.get('password1')
            user_account.set_password(password)
            user_account.save()
            print("User account saved:", user_account)
            return redirect('user-list')
        else:
            messages.error(request, f"Error adding new user. {form.errors}")
            return redirect('/account/add')
    context = {
        "form": form
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def view_account(request,pk):
    template_name = 'accounts/view_account.html'
    account = User.objects.filter(id=pk)
    context = {
        "account": account
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def update_account(request, pk):
    template_name = 'accounts/update_account.html'
    account = get_object_or_404(User, id=pk)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('user-list')
    context = {
        "form": form,
        "pk": pk
    }
    return render(request, template_name, context)


#functions for PROFILE
@login_required(login_url='/login')
def profile(request):
    pk = request.user.id
    template_name = 'accounts/profile.html'
    user_data = User.objects.filter(id=request.user.id)
    context = {
        "user_data": user_data,
        "pk": pk
    }
    return render(request, template_name, context)

#functions for CHANGE/UPDATE PASSWORD
@login_required(login_url='/login')
def password_update(request):
    template_name = 'accounts/update_pass.html'
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "Passwords doesn't match")
        else:
            try:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully.')
                return redirect("/")
            except User.DoesNotExist:
                messages.error(request, "User doesn't exists")
    context = {
        "pk": request.user.id
    }
    return render(request, template_name, context)


@login_required(login_url='/login')
def incoming_docs(request):
    template_name= "incoming_docs/incoming.html"
    user = User.objects.filter(id=request.user.id).first()
    document = OutgoingDocs.objects.filter(forwarded_to = user.department).order_by('-date_created')
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    print(user.department)
    context = {
        "document": document,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def tracking_list(request, pk):
    template_name = "tracking/tracking_list.html"
    tracking = Tracking.objects.filter(docs=pk).order_by("-created")

    context = {
        "tracking" : tracking
    }  
    return render(request, template_name, context)

@login_required(login_url='/login')
def delete_category(request, pk):
    Category.objects.filter(id=pk).delete()

    return redirect("/category/list")


def notifications_list(request):
    notifications = Notifications.objects.filter(department=request.user.department).order_by("-created_at")
    context = {
        "notifications" : notifications
    }
    return render(request, "notifications/notifications_list.html", context)


@login_required(login_url='/login')
def delete_account(request,pk):
    """
    This function deletes a user account with a specific primary key and redirects to the accounts list
    page.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted in the request, and more
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific user account in the database. The function is designed to delete the user account with the
    specified primary key (pk) and then redirect the user to the list of all remaining user accounts
    :return: a redirect to the 'accounts-list' URL after deleting the user account with the primary key
    (pk) specified in the request.
    """
    account = User.objects.filter(id=pk)
    account.delete()
    return redirect('account')


@login_required(login_url='/login')
def document_status(request):
    template_name= "incoming_docs/document_status.html"
    document = OutgoingDocs.objects.all().order_by('-date_created')
    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    document = paginator.get_page(page_number)
    context = {
        "document": document,
    }
    return render(request, template_name, context)

@login_required(login_url='/login')
def delete_department(request, pk):
    """
    The function "delete_department" takes in a request and a primary key (pk) as parameters and likely
    deletes a department object from a database based on the pk.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), any data submitted with the request, and the user's session information
    :param pk: "pk" stands for "primary key". In Django, the primary key is a unique identifier for each
    record in a database table. In this case, "pk" is the primary key of the department that needs to be
    deleted
    """
    department = Department.objects.filter(id=pk)
    department.delete()
    return redirect('department-list')
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#form for login
class LoginForm(forms.Form):
    employee_no = forms.CharField(label='Employee No')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control"}),
    )
 
    class Meta:
        fields = ['employee_no', 'password']

#form for outgoing documents
class OutgoingDocsForm(forms.ModelForm):
    document = forms.FileField(
        label='Select a PDF file',
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
    )
    forwarded_to = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Please select office:")
    type_of_document = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select document type:")
    

    class Meta:
        model = OutgoingDocs
        fields = ['title_docs', 'type_of_document', 'forwarded_to', 'status','document']

    def clean_document(self):
        document = self.cleaned_data['document']
        if not document.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")
        return document

#form for release of incoming documents
class ReleaseForm(forms.ModelForm): 
    forwarded_to = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Please select office:")
    class Meta:
        model = OutgoingDocs
        fields = ['doc_actions', 'forwarded_to', 'document']

#form for incoming documents    
# class IncomingDocsForm(forms.ModelForm):
#     class Meta:
#         model = IncomingDocs
#         fields = ['receiver', 'doc_actions']

#form for document type
class CategoryForm(forms.ModelForm):
    category =  forms.CharField(label="Document Type")
    
    class Meta:
        model = Category
        fields = '__all__'

#form for department
class DepartmentForm(forms.ModelForm):  
    class Meta:
        model = Department
        fields = '__all__'

#form for user
user_type = (
    ('', 'Select User Type'),
    ('Admin', 'Admin'),
    ('Employee', 'Employee'),
)
class UserForm(UserCreationForm):
    user_type = forms.ChoiceField(label="This account is for : ", choices=user_type)
    class Meta:
        model = User
        fields = ['profile_picture', 'employee_no', 'user_type', 'department', 'first_name', 'last_name', 'contact'] 
   
class UserUpdateForm(forms.ModelForm):
    employee_no = forms.CharField(disabled=True)
    phone_regex = RegexValidator(r'^\d{11}$', 'Phone number must be 11 digits long.')

    contact = forms.CharField(max_length=11, validators=[phone_regex], label="Contact Number: (Format:09xxxxxxxxx)")
    class Meta:
        model = User
        fields = ['profile_picture', 'employee_no', 'first_name', 'last_name', 'contact'] 
        exclude = ('user_type',)
    
 

   
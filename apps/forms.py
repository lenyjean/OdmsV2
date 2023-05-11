from django import forms
from .models import *
from django.core.exceptions import ValidationError

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

    class Meta:
        model = OutgoingDocs
        fields = ['title_docs', 'type_of_document', 'forwarded_to', 'status',]

    def clean_document(self):
        document = self.cleaned_data['document']
        if not document.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")
        return document

#form for release of incoming documents
class ReleaseForm(forms.ModelForm): 
    class Meta:
        model = OutgoingDocs
        fields = ['doc_actions', 'forwarded_to']

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
   
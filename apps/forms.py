from django import forms

class LoginForm(forms.Form):
    employee_no = forms.CharField(label='Employee No')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class" : "form-control"}),
    )
 
    class Meta:
        fields = ['employee_no', 'password']
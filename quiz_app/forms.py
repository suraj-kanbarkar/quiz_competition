from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    psw = forms.PasswordInput()
    psw_repeat = forms.PasswordInput()


class SignIn(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    psw = forms.PasswordInput()

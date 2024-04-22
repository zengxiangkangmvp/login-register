from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    captcha = CaptchaField(label='验证码')


class RegisterFrom(forms.Form):
    GENDERS = [
        (0, '未知'),
        (1, '男性'),
        (2, '女性'),
    ]

    username = forms.CharField(
        label='用户名',
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='确认密码',
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='邮箱地址',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='性别',
        choices=GENDERS
    )
    captcha = CaptchaField(label='验证码')
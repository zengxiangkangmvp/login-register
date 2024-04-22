import hashlib
from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives

# Create your views here.

from . import models
from . import forms


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_code(user: models.User):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.username, now)
    models.Confirm.objects.create(user=user, code=code)
    return code


def send_email(email, code):
    subject = '来自www.liujiangblog.com的注册确认邮件'
    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                      如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def index(request):
    if not request.session.get('login', False):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('login', False):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(username=username)
            except :
                return render(request, 'login/login.html', {'login_form': login_form, 'message': '用户不存在'})
            if not user.has_confirmed:
                return  render(request, 'login/login.html', {'login_form': login_form, 'message': '邮箱未确认'})
            if user.password == hash_code(password):
                request.session['login'] = True
                request.session['userid'] = user.id
                request.session['username'] = user.username
                return redirect('/index/')
            else:
                return render(request, 'login/login.html', {'login_form': login_form, 'message': '密码不正确'})
        else:
            return render(request, 'login/login.html', {'login_form': login_form, 'message': '验证不通过'})
    login_form = forms.UserForm()
    return render(request, 'login/login.html', {'login_form': login_form})


def register(request):
    if request.session.get('login', False):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterFrom(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:
                return render(request, 'login/register.html', {'register_form': register_form, 'message': '密码不一致'})
            filter_user = models.User.objects.filter(username=username)
            if filter_user:
                return render(request, 'login/register.html', {'register_form': register_form, 'message': '用户已注册'})
            filter_email = models.User.objects.filter(email=email)
            if filter_email:
                return render(request, 'login/register.html', {'register_form': register_form, 'message': '邮箱已注册'})
            user = models.User.objects.create(username=username, password=hash_code(password1), email=email, sex=sex)
            code = make_confirm_code(user)
            send_email(email, code)
            return render(request, 'login/confirm.html', {'register_form': register_form, 'message': '请前往邮箱进行确认'})
        else:
            return render(request, 'login/register.html', {'register_form': register_form, 'message': '验证不通过'})
    register_form = forms.RegisterFrom()
    return render(request, 'login/register.html', {'register_form': register_form})


def confirm(request):
    code = request.GET.get('code', None)
    try:
        confirm = models.Confirm.objects.get(code=code)
    except:
        return render(request, 'login/confirm.html', {'message': '无效确认码'})
    create_time = confirm.created_time
    now = datetime.now()
    if now > create_time + timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        return render(request, 'login/confirm.html', {'message': '验证已过期'})
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        return render(request, 'login/confirm.html', {'message': '邮箱已确认'})


def logout(request):
    if not request.session.get('login', False):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')


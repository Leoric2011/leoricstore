# !/usr/bin/python3.6
# -*- coding: utf-8 -*-
'''
File: views.py
Project: Tango with Django 2.0
File Created: Thursday, 3rd May 2018 12:41:48 pm
Author: Dennis, Wangyi (denniswangyi@gmail.com)
-----
Last Modified: Saturday, 12th May 2018 6:30:59 pm
Modified By: Dennis, Wangyi (denniswangyi@gmail.com>)
-----
Copyright 2018 - 2018 Dennis, Wangyi
'''
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler_serverside(request):
    vistis = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        vistis = vistis + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = vistis


def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)
    response.set_cookie('visits', visits)

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visitor_cookie_handler_serverside(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    # print(request.method)
    # print(request.user)
    context_dict = {'developer_name': 'Dennis'}

    visitor_cookie_handler_serverside(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # 用来返回给模版文件注册是否成功的标识变量。
    # 初始设置为 False， 注册成功后设置为 True
    registed = False

    # 如果请求的类型是 POST， 那么我们将对提交的注册信息进行处理
    if request.method == 'POST':
        # 试图从原始提交的表格信息中提取有用的信息
        # 需要注意的是我们同时需要 UserForm 和 UserProfileForm的信息
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # 假如两个 Form的数据都通过校验...
        if user_form.is_valid() and profile_form.is_valid():
            # 将用户注册 Form 中的信息直接存入数据库
            user = user_form.save()

            # 使用 set_password方法，来对用户的密码进行哈希算法的加密
            # 加密完成后，应该更新用户的密码数据，以在数据库中保存
            user.set_password(user.password)
            user.save()

            # 现在开始处理用户档案数据的Form信息，因为我们还需要补充输入相关的属性数据
            # 所以我们在这里设置 commit=False ，来延迟数据被直接存入数据库
            # 当我们完成所有的设置工作后，再真正提交数据库保存，这样能保证数据的完整性，避免异常的BUG
            profile = profile_form.save(commit=False)
            profile.user = user

            # 在这里我们判断用户是否上传了头像图片
            # 如果用户上传了，那么我们需要从提交Form的数据中取出文件，并更新到我们的用户档案model中去
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # 现在我们对用户档案的模型进行保存，即存入了数据库
            profile.save()

            # 更新标识变量，以告诉模板我们已经注册成功了
            registed = True
        else:
            # 如果 Form 数据校验不通过——存在某些错误
            # 在 Terminal 中将错误打印出来
            print(user_form.errors, profile_form.errors)
    else:
        # 如果请求类型不是 POST，那么我们将用使用两个 ModelForm 的实例来进行模板渲染
        # 并且这两个实例的数据为空
        user_form = UserForm()
        profile_form = UserProfileForm()

    # 返回模板渲染，并传入上下文参数
    return render(
        request,
        'rango/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registed': registed
        }
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            error_msg = 'Your Rango account is disabled.'
            return render(request, 'rango/login.html', {'error_msg': error_msg})
        error_msg = "Invalid login detail supplied. "
        return render(request, 'rango/login.html', {'error_msg': error_msg})
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

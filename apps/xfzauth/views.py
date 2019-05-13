from io import BytesIO

from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from apps.xfzauth.models import User
from utils import restful
from django.views.decorators.http import require_POST

from apps.xfzauth.forms import LoginForm, RegisterForm
from utils.captcha.xfzcaptcha import Captcha


@require_POST  # 限制为post请求
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)  # django 登录
                if remember:  # 是否记住
                    request.session.set_expiry(None)  # 使用django默认的过期时间两个星期
                else:
                    request.session.set_expiry(0)  # 浏览器关闭就过期
                return restful.ok()
                # return JsonResponse({'code': 200, 'message': '', 'date': {}}) 使用的restful封装烟返回的错误信息
            else:
                return restful.unauth(message='您的账号已冻结')
        else:
            return restful.params_error(message='手机号或者密码错误')
    else:
        errors = form.get_errors()  # 获取验证错误信息
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


# 注册
@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request, user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())


# 图形验证码
def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    # 12Df：12Df.lower()
    # cache.set(text.lower(), text.lower(), 5 * 60)
    return response

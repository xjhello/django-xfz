from django.shortcuts import render
from .models import Payinfo,PayinfoOrder
from apps.xfzauth.decorators import xfz_login_required
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from django.shortcuts import reverse
from django.http import FileResponse,Http404
from django.conf import settings
import os


#  付费文档主页
def index(request):
    context = {
        'payinfos': Payinfo.objects.all()
    }
    return render(request,'payinfo/payinfo.html',context=context)


@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    order = PayinfoOrder.objects.create(payinfo=payinfo,buyer=request.user,status=1,amount=payinfo.price)
    context = {
        'goods': {
            'thumbnail': '',
            'price': payinfo.price,
            'title': payinfo.title
        },
        'order': order,
        'notify_url':request.build_absolute_uri(reverse('payinfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payinfo:index'))
    }
    return render(request,'course/course_order.html',context=context)


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get("orderid")
    PayinfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()


# 文档下载
@xfz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    order = PayinfoOrder.objects.filter(payinfo_id=payinfo_id,buyer=request.user,status=2).first()
    if order:
        payinfo = order.payinfo
        path = payinfo.path
        # /a/xx.png = ['',a,xx.png]
        fp = open(os.path.join(settings.MEDIA_ROOT,path),'rb')
        response = FileResponse(fp)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment;filename="%s"' % path.split("/")[-1]
        return response
    else:
        return Http404()
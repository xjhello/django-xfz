from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from apps.news.forms import PublicCommentForm
from apps.news.models import News, NewsCategory, Comment, Banner
from apps.news.serializers import NewsSerializer, CommentSerizlizer
from apps.xfzauth.decorators import xfz_login_required
from utils import restful


# 新闻主页
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').order_by('-pub_time')[0:count]  # 时间倒叙排序
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': banners
    }
    return render(request, 'news/index.html', context=context)


# 获取新闻列表
def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p', 1))  # 1为默认值
    # 默认分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT  # 开始页数
    end = start + settings.ONE_PAGE_NEWS_COUNT  # 结束页数

    if category_id == 0:  # 获取所有的数据
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:  # select_related：在提取某个模型的数据的同时，也提前将相关联的数据提取出来
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)  # many指有多个
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request,'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


# 评论
@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)  # 搜索新闻
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
    return render(request, 'search/search1.html', context=context)
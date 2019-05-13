from django.urls import path
from .import views

app_name = 'news'  # 避免url名字重复，使用应用命名空间，使用：news:index
urlpatterns = [
    # path('', views.index, name='index'),  # name为此url命名，index=''
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('list/', views.news_list, name='news_list'),
    path('public_comment/', views.public_comment, name='public_comment')
]
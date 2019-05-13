from rest_framework import serializers
from .models import News, NewsCategory, Comment, Banner
from apps.xfzauth.serializers import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory  # 指明模型
        fields = ('id', 'name')  # 指明所要序列化的字段


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()  # 类别外键,获取的不再是id 而是category表的完整字段内容
    author = UserSerializer()  # 作者外键

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author')


class CommentSerizlizer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'priority', 'link_to')

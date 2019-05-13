from haystack import indexes
from .models import News


#  搜索索引设置文件 名字必须为search_indexes
class NewsIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 索引主要字段，默认取名text,想要更改要在setting中设置。

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
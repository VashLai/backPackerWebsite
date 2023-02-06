from operator import index
from django.db import models
from index.models import Backpacker
from user.models import User

# Create your models here.


class Favorite(models.Model):
    # title = models.CharField(max_length=100, verbose_name='主題')
    article_id = models.CharField(max_length=20, null=False, default= 'nono', verbose_name='文章號')
    bparticlenum = models.ManyToManyField(Backpacker, related_name='bparticlenum',verbose_name='文章編號')
    note = models.TextField()
    b_time = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    c_time = models.DateTimeField(auto_now=True, verbose_name='修改時間')
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        # print(backpacker.title for backpacker in self.bparticlenum.all())
        return "%s(%s)" % ('我的最愛:',",".join(backpacker.title for backpacker in self.bparticlenum.all()),)

    class Meta:
        db_table = 'favorite'
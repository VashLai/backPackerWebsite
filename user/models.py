from django.db import models
from psutil import users

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20,verbose_name='使用者名稱')
    email = models.EmailField(max_length=50,unique=True,verbose_name='電子郵件')
    password = models.CharField(max_length=32,verbose_name='密碼')

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'

    
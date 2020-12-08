from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''ユーザー作成日を追加したユーザーモデル'''

    image = models.ImageField(verbose_name='ユーザー画像', upload_to='user', max_length=100, null=True, blank=True)
    describe = models.TextField(verbose_name='プロフィール', max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.username

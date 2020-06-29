from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''ユーザー作成日を追加したユーザーモデル'''

    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
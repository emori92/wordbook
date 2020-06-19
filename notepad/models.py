from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    '''ユーザー作成日を追加したユーザーモデル'''
    class Meta:
        db_table = 'ユーザー'
        
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    
    def __str__(self):
        return self.username


# class Tag(models.Model):
#     '''ノートをカテゴリするタグのモデル'''
#     class Meta:
#         db_table = 'カテゴリタグ'
        
#     tag_name = models.CharField(verbose_name='カテゴリタグ', max_length=32)

#     def __str__(self):
#         return self.tag_name


class Note(models.Model):
    '''メモ基本情報のモデル'''
    class Meta:
        db_table = 'ノート'
        
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    # tag = models.ForeignKey(Tag, verbose_name='カテゴリ', on_delete=models.PROTECT, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=16)
    describe = models.TextField(verbose_name='説明')
    # public = models.BooleanField(verbose_name='公開範囲')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    # updated_at = models.DateTimeField(verbose_name='更新日', null=True)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    '''問題、ヒント、答えのモデル'''
    class Meta:
        db_table = '問題'
        
    query = models.CharField(verbose_name='問題', max_length=256)
    hint = models.CharField(verbose_name='ヒント', max_length=64, null=True)
    answer = models.CharField(verbose_name='答え', max_length=256)
    # review = models.BooleanField(verbose_name='復習', )
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    # updated_at = models.DateTimeField(verbose_name='更新日', )
    note = models.ForeignKey(Note, verbose_name='ノート', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.query


# class Star(models.Model):
#     '''ノートをブックマークするモデル'''
#     class Meta:
#         db_table = 'ブックマーク'

#     note = models.ForeignKey(Note, verbose_name='ノート', on_delete=models.PROTECT)
#     user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)

#     def __str__(self):
#         return self.note
    

# class Follower(models.Model):
#     '''フォロワーのモデル'''
#     class Meta:
#         db_table = 'フォロワー'

#     following = models.ForeignKey(User, verbose_name='フォロー', on_delete=models.PROTECT)
#     followed = models.ForeignKey(User, verbose_name='フォロワー', on_delete=models.PROTECT)

#     def __str__(self):
#         return self.following
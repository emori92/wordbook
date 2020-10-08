from django.db import models

from accounts.models import User


class Tag(models.Model):
    '''ノートをカテゴリするタグのモデル'''

    name = models.CharField(verbose_name='タグ', max_length=32, unique=True)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class Note(models.Model):
    '''メモ基本情報のモデル'''

    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='タグ')
    title = models.CharField(verbose_name='タイトル', max_length=32)
    describe = models.TextField(verbose_name='説明', max_length=128, null=True, blank=True)
    public = models.BooleanField(verbose_name='公開範囲', default=0)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        db_table = 'note'
    
    def __str__(self):
        return self.title


class Question(models.Model):
    '''問題、ヒント、答えのモデル'''

    question = models.TextField(verbose_name='問題', max_length=128)
    hint = models.TextField(verbose_name='ヒント', max_length=64, null=True, blank=True)
    answer = models.TextField(verbose_name='答え', max_length=256)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
    note = models.ForeignKey(Note, verbose_name='ノート', on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'
    
    def __str__(self):
        return self.question


class Review(models.Model):
    """問題を復習する"""

    question = models.ForeignKey(Question, verbose_name='問題', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'"{self.question}/{self.user}"'


class Star(models.Model):
    '''ノートをブックマークするモデル'''

    note = models.ForeignKey(Note, verbose_name='ノート', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(verbose_name='いいねした日', auto_now=True)

    class Meta:
        db_table = 'star'

    def __str__(self):
        return self.note


class Follow(models.Model):
    '''フォロワーのモデル'''

    following = models.ForeignKey(User, verbose_name='フォローした人', related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, verbose_name='フォローされた人', related_name='followed', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(verbose_name='フォローした日', auto_now_add=True)
    
    class Meta:
        db_table = 'follow'

    def __str__(self):
        return self.following

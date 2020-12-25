## Wordbook
単語帳を作成できるWebアプリケーションです。単語帳を作成し、問題、ヒント、回答を自由に作成できます。
Python製WebフレームワークのDjangoで作成しています。

## 環境
- OS: Catalina 10.15.7
- Docker: 19.03.13
- docker-compose: 1.27.4
- Python: 3.7.9
- Django: 2.2.16
- PostgreSQL: 12.5
- Nginx: 1.19.5
- AWS: IAM, VPC, EC2, S3
- SSH: Let's Encrypt

## 機能
- サインアップ/ログイン/ログアウト
- ユーザーフォロー
- 単語帳/ユーザー/タグの検索
- 単語帳のタグ機能
- 単語帳の公開範囲
- 単語帳のいいね
- フォロー/いいねした単語帳の一覧
- 復習したい問題の選択

## パッケージ
- django-debug-toolbar 2.2
- django-environ       0.4.5
- django-sass          1.0.0
- django-crispy-forms  1.9.2
- django-storages      1.11.1
- psycopg2-binary      2.8.5
- gunicorn             20.0.4
- whitenoise           5.2.0
- selenium             3.141.0

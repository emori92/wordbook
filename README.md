## Wordbook
単語帳を作成できるWebアプリケーションです。単語帳を作成し、問題、ヒント、回答を自由に作成できます。
Python製WebフレームワークのDjangoで作成しています。

## 環境
- OS: Catalina 10.15.7
- Docker: 20.10.0
- docker-compose: 1.27.4
- Python: 3.7.9
- Django: 2.2.17
- PostgreSQL: 12.5
- Nginx: 1.19.5
- AWS: IAM, VPC, EC2, S3, ECR
- Domain: freenom
- SSL: certbot

## 機能
- 新規登録/ログイン/ログアウト
- ユーザーフォロー
- 単語帳/ユーザー/タグの検索
- 単語帳のタグ付け
- 単語帳の非公開
- 単語帳のいいね
- フォロー/いいねした単語帳の一覧
- 復習したい問題の選択
- ページネーション
- JavaScriptによる表示切り替え

## パッケージ
- django-debug-toolbar 2.2
- django-environ       0.4.5
- django-sass          1.0.0
- django-crispy-forms  1.9.2
- django-storages      1.11.1
- boto3                1.16.43
- psycopg2-binary      2.8.5
- gunicorn             20.0.4
- whitenoise           5.2.0
- selenium             3.141.0

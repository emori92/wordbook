# Wordbook

単語帳を作成できるWebアプリケーションです。単語帳を作成し、問題、ヒント、回答を自由に作成できます。Python製WebフレームワークのDjangoで作成しています。

![play-wordbook](https://user-images.githubusercontent.com/36121673/106491297-0f866680-64fa-11eb-807b-35ff503f5673.gif)

---

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

## 開発環境

- OS: Catalina 10.15.7
- Docker: 20.10.7
- docker-compose: 1.29.2
- Python: 3.7.9
- Django: 2.2.24
- Bootstrap: 4.5.0
- PostgreSQL: 12.5
- Nginx: 1.19.5

## インフラ

- AWS: IAM, VPC, EC2, S3
- GCP: IAM, VPC, GCE, GCS
- Domain: freenom
- DNS: freenom
- SSL: certbot
- Analytics: Google Analytics

---

## インフラ構成図

### AWS

![aws-architecture-figure](https://user-images.githubusercontent.com/36121673/106470096-764c5580-64e3-11eb-8c5f-3d0020ccfc55.png)

### GCP

![gcp-architecture-figure](https://user-images.githubusercontent.com/36121673/106470626-0e4a3f00-64e4-11eb-9b6c-5d9b96dce302.png)

---

## パッケージ

- django-debug-toolbar  2.2.1
- django-environ        0.4.5
- django-sass           1.0.0
- django-crispy-forms   1.9.2
- django-storages       1.11.1
- boto3                 1.16.43
- google-cloud-storage  1.35.0
- psycopg2-binary       2.8.5
- gunicorn              20.0.4
- whitenoise            5.2.0
- selenium              3.141.0

---

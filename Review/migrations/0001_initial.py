# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book_name', models.CharField(max_length=255)),
                ('date_of_add', models.DateField(default=b'Indian')),
                ('description', models.TextField()),
                ('author', models.TextField()),
                ('image', models.ImageField(upload_to=b'book')),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('book_id', models.ForeignKey(to='Review.BookInfo')),
            ],
        ),
        migrations.CreateModel(
            name='DisLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dislike', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('book_id', models.ForeignKey(to='Review.BookInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review', models.TextField()),
                ('book_id', models.ForeignKey(to='Review.BookInfo')),
            ],
        ),
        migrations.CreateModel(
            name='SoftBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.FileField(upload_to=b'softcopy')),
                ('book_id', models.ForeignKey(to='Review.BookInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('confirm_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UsersFavourite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.TextField()),
                ('booktype', models.ForeignKey(to='Review.BookType')),
                ('userid', models.ForeignKey(to='Review.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='softbook',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='like',
            name='review_id',
            field=models.ForeignKey(to='Review.Review'),
        ),
        migrations.AddField(
            model_name='like',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='dislike',
            name='review_id',
            field=models.ForeignKey(to='Review.Review'),
        ),
        migrations.AddField(
            model_name='dislike',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='comments',
            name='review_id',
            field=models.ForeignKey(to='Review.Review'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='book_type',
            field=models.ForeignKey(to='Review.BookType'),
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='user_id',
            field=models.ForeignKey(to='Review.UserInfo'),
        ),
    ]

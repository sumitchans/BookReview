# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.FileField(upload_to=b'softcopy')),
                ('book_id', models.ForeignKey(to='Review.BookInfo')),
                ('user_id', models.ForeignKey(to='Review.UserInfo')),
            ],
        ),
    ]

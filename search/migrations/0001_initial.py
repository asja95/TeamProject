# Generated by Django 3.1 on 2020-09-02 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=20, verbose_name='아티스트')),
                ('image', models.CharField(max_length=20, verbose_name='포스터')),
                ('artist_id', models.IntegerField(verbose_name='아티스트번호')),
            ],
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(max_length=50, verbose_name='제목')),
                ('artist', models.CharField(max_length=20, verbose_name='가수')),
                ('release', models.CharField(max_length=10, verbose_name='발매날짜')),
                ('genre', models.CharField(max_length=10, verbose_name='장르')),
            ],
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(max_length=50, verbose_name='제목')),
                ('album', models.CharField(max_length=50, verbose_name='앨범')),
                ('artist', models.CharField(max_length=20, verbose_name='가수')),
                ('image', models.CharField(max_length=20, verbose_name='포스터')),
                ('lyrics', models.TextField(max_length=5000, verbose_name='가사')),
                ('release', models.CharField(max_length=10, verbose_name='발매날짜')),
                ('genre', models.CharField(max_length=20, verbose_name='장르')),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, verbose_name='번호')),
                ('name', models.CharField(max_length=20, verbose_name='장르')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(max_length=50, verbose_name='제목')),
                ('album', models.CharField(max_length=50, verbose_name='앨범')),
                ('artist', models.CharField(max_length=20, verbose_name='가수')),
                ('lyrics', models.TextField(max_length=5000, verbose_name='가사')),
                ('release', models.CharField(max_length=10, verbose_name='발매날짜')),
                ('genre', models.CharField(max_length=20, verbose_name='장르')),
                ('type', models.CharField(max_length=10, verbose_name='테마')),
            ],
        ),
    ]

# Generated by Django 3.0.1 on 2019-12-30 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=250)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
    ]
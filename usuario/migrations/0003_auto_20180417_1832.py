# Generated by Django 2.0.4 on 2018-04-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20180417_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='cidade',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='perfil',
            name='dn',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='capa',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='sobre',
            field=models.TextField(blank=True),
        ),
    ]
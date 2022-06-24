# Generated by Django 4.0.2 on 2022-06-14 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humancapital', '0007_employee_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='qid',
            field=models.CharField(default=12, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='qid_img',
            field=models.ImageField(default='jdhf.img', upload_to='qid_%Y-%m-%d'),
            preserve_default=False,
        ),
    ]

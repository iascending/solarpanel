# Generated by Django 2.2.2 on 2019-08-24 12:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20190824_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='dateCreate',
            field=models.DateField(auto_now_add=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='installation',
            name='dateInstall',
            field=models.DateField(default=datetime.date.today, verbose_name='Date Installed'),
        ),
        migrations.AlterField(
            model_name='installation',
            name='dateUpdate',
            field=models.DateField(auto_now=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='installation',
            name='inspectFile',
            field=models.FileField(blank=True, upload_to=projects.models.Installation.get_inspectfile_upload_path, verbose_name='Inspection Report'),
        ),
        migrations.AlterField(
            model_name='installation',
            name='installFile',
            field=models.FileField(blank=True, upload_to=projects.models.Installation.get_installfile_upload_path, verbose_name='Installation Report'),
        ),
        migrations.AlterField(
            model_name='paperwork',
            name='install',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pw_for_install', to='projects.Installation', verbose_name='Installation'),
        ),
    ]
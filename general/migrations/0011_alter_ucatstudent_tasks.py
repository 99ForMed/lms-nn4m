# Generated by Django 4.1.7 on 2023-02-17 13:00

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0010_alter_ucatstudent_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucatstudent',
            name='tasks',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None),
        ),
    ]

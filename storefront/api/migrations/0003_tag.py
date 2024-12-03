# Generated by Django 5.1.3 on 2024-12-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_note_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('notes', models.ManyToManyField(related_name='tags', to='api.note')),
            ],
        ),
    ]

# Generated by Django 3.2.22 on 2023-11-13 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0004_auto_20230727_2054'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_overviews', '0029_alter_historicalcourseoverview_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_overviews.courseoverview')),
                ('org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_roles.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'role', 'course')},
            },
        ),
        migrations.CreateModel(
            name='RoleService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_roles.role')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_roles.service')),
            ],
        ),
        migrations.CreateModel(
            name='RolePermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_roles.permission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_roles.role')),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(through='course_roles.RolePermissions', to='course_roles.Permission'),
        ),
        migrations.AddField(
            model_name='role',
            name='services',
            field=models.ManyToManyField(through='course_roles.RoleService', to='course_roles.Service'),
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(through='course_roles.UserRole', to=settings.AUTH_USER_MODEL),
        ),
    ]

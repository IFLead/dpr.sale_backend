# Generated by Django 2.0.8 on 2018-10-10 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Имя')),
                ('decription', models.TextField(max_length=256, verbose_name='Описание')),
                ('phone_one', models.CharField(blank=True, max_length=25, null=True, verbose_name='Первый номер телефона')),
                ('phone_two', models.CharField(blank=True, max_length=25, null=True, verbose_name='Второй номер телефона')),
                ('phone_three', models.CharField(blank=True, max_length=25, null=True, verbose_name='Третий номер телефона')),
                ('phone_four', models.CharField(blank=True, max_length=25, null=True, verbose_name='Четвёртый номер телефона')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('symbol', models.CharField(max_length=3, verbose_name='Символ')),
                ('is_prefix', models.BooleanField(default=False, verbose_name='Префиксный символ')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='CustomData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=25, null=True, verbose_name='Номер телефона')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Доп информация о пользователе',
                'verbose_name_plural': 'Доп информация о пользователе',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Название')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district', to='Main.City', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Районы',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(max_length=255, upload_to='img/%Y/%m/%d', verbose_name='Изображение')),
                ('sort_order', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_top', models.BooleanField(default=False, verbose_name='Рекомендованное')),
                ('closed', models.BooleanField(default=False, verbose_name='Закрыто')),
                ('is_archive', models.BooleanField(default=False, verbose_name='В архиве')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True, verbose_name='Стоимость')),
                ('rooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество комнат')),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Этаж')),
                ('storeys', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Этажность здания')),
                ('landmark', models.CharField(blank=True, max_length=256, null=True, verbose_name='Ориентир')),
                ('total_square', models.FloatField(blank=True, null=True, verbose_name='Общая площадь (метры кв.)')),
                ('living_square', models.FloatField(blank=True, null=True, verbose_name='Жилая площадь (метры кв.)')),
                ('kitchen_square', models.FloatField(blank=True, null=True, verbose_name='Кухонная площадь (метры кв.)')),
                ('corner', models.BooleanField(default=False, verbose_name='Угловая')),
                ('balcony', models.NullBooleanField(verbose_name='Балкон застеклён')),
                ('loggia', models.NullBooleanField(verbose_name='Лоджия застеклена')),
                ('created', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('contacts', models.TextField(blank=True, help_text='Не отображается на сайте', null=True, verbose_name='Контакты')),
                ('private_description', models.TextField(blank=True, help_text='Не отображается на сайте', null=True, verbose_name='Комментарии от риелтора')),
                ('address', models.TextField(blank=True, help_text='Не отображается на сайте', null=True, verbose_name='Адрес')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Состояние',
                'verbose_name_plural': 'Состояния',
            },
        ),
        migrations.CreateModel(
            name='TreeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Main.TreeCategory')),
            ],
            options={
                'verbose_name': 'Тип недвижимости',
                'verbose_name_plural': 'Типы недвижимости',
            },
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Окно',
                'verbose_name_plural': 'Окна',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='category_tree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.TreeCategory', verbose_name='Тип недвижимости'),
        ),
        migrations.AddField(
            model_name='post',
            name='currency_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Main.Currency', verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='post',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.Client', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='post',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='Main.District', verbose_name='Район'),
        ),
        migrations.AddField(
            model_name='post',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.Material', verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(on_delete=models.SET(43), to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='post',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.State', verbose_name='Состояние'),
        ),
        migrations.AddField(
            model_name='post',
            name='window',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.Window', verbose_name='Окно'),
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Main.Post'),
        ),
    ]

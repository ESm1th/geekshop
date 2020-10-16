# Generated by Django 2.1.4 on 2018-12-11 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort', models.IntegerField(blank=True, default=0, null=True, verbose_name='sort')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('kind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort', models.IntegerField(blank=True, default=0, null=True, verbose_name='sort')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('picture', models.ImageField(max_length=250, upload_to='media/images', verbose_name='picture')),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort', models.IntegerField(blank=True, default=0, null=True, verbose_name='sort')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
            ],
            options={
                'verbose_name': 'Manufacturer',
                'verbose_name_plural': 'Manufacturers',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort', models.IntegerField(blank=True, default=0, null=True, verbose_name='sort')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, verbose_name='Quantity on stock')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Manufacturer')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='mainapp.Product'),
        ),
    ]
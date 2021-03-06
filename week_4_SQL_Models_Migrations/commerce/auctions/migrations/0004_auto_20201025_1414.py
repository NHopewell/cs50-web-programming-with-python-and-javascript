# Generated by Django 3.1.2 on 2020-10-25 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201021_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('1', 'Art & Collectibles'), ('2', 'Clothing'), ('3', 'Electronics'), ('4', 'Health & Beauty'), ('5', 'Home & Yard'), ('6', 'Jewellery'), ('7', 'Sporting Goods')], max_length=30),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='default.png', upload_to='listing_pics'),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated manually for Payment model (Razorpay)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100, unique=True)),
                ('amount_paise', models.PositiveIntegerField()),
                ('amount_inr', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(default='created', max_length=20)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_signature', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('packing', '0006_orderitem_picked'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.AddField(model_name='order', name='customer', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packing_orders', to=settings.AUTH_USER_MODEL)),
        migrations.AddField(model_name='order', name='delivery_address', field=models.TextField(blank=True)),
        migrations.AddField(model_name='order', name='delivery_phone', field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='order', name='delivery_person', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='order', name='delivery_person_phone', field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name='order', name='delivery_latitude', field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        migrations.AddField(model_name='order', name='delivery_longitude', field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        migrations.AddField(model_name='order', name='estimated_delivery', field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name='order', name='payment_status', field=models.CharField(choices=[('pending', 'Pending'), ('paid_demo', 'Paid (demo)'), ('failed', 'Failed'), ('cod', 'Cash on delivery')], default='pending', max_length=20)),
        migrations.CreateModel(name='CustomerProfile', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('role', models.CharField(choices=[('customer', 'Customer'), ('warehouse', 'Warehouse staff')], default='customer', max_length=20)), ('phone', models.CharField(blank=True, max_length=20)), ('address', models.TextField(blank=True)), ('notifications_enabled', models.BooleanField(default=True)), ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='WishlistItem', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('created_at', models.DateTimeField(auto_now_add=True)), ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packing.product')), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to=settings.AUTH_USER_MODEL))], options={'unique_together': {('user', 'product')}}),
        migrations.CreateModel(name='SupportTicket', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('subject', models.CharField(max_length=120)), ('message', models.TextField()), ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In progress'), ('resolved', 'Resolved')], default='open', max_length=20)), ('staff_reply', models.TextField(blank=True)), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)), ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='packing.order')), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_tickets', to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='UserNotification', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('title', models.CharField(max_length=120)), ('message', models.CharField(max_length=300)), ('is_read', models.BooleanField(default=False)), ('created_at', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quickpack_notifications', to=settings.AUTH_USER_MODEL))]),
    ]

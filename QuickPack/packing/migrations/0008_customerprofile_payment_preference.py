from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("packing", "0007_customer_warehouse_features")]
    operations = [migrations.AddField(
        model_name="customerprofile",
        name="payment_preference",
        field=models.CharField(choices=[("cod", "Cash on delivery"), ("upi", "UPI (demo preference)"), ("card", "Card (demo preference)")], default="cod", max_length=20),
    )]

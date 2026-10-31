from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("packing", "0013_alter_box_id_alter_customerprofile_id_alter_order_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_location_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

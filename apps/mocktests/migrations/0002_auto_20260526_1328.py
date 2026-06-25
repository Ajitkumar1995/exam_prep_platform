from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mocktests", "0001_initial"),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name="mocktest",
            name="is_free",
            field=models.BooleanField(
                default=True, help_text="If True, test is free to take"
            ),
        ),
    ]

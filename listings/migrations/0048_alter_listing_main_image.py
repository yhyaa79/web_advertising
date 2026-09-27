from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0047_alter_category_platform_alter_listing_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="main_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="listings/images/",
                verbose_name="تصویر اصلی",
            ),
        ),
    ]

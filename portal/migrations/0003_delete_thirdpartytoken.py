# Generated by Django 4.2.5 on 2023-10-22 20:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("portal", "0002_thirdpartytoken"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ThirdPartyToken",
        ),
    ]
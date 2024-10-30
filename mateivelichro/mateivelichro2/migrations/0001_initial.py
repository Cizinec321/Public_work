# Generated by Django 3.2.18 on 2024-10-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='co2_items_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=250)),
                ('item_unit', models.CharField(max_length=25)),
                ('item_co2perunit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='co2_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(202409, 202409), (202410, 202410), (202411, 202411)])),
                ('item_name', models.CharField(choices=[('LPG', 'LPG'), ('Gasoline', 'Gasoline'), ('Elec_ap8', 'Electricity for ap. 8'), ('Elec_ap20', 'Electricity for ap. 20'), ('Gas_ap8', 'Gas for ap. 8'), ('Gas_ap20', 'Gas for ap. 20'), ('Work_flight', 'Work flights'), ('Leisure_flight', 'Leisure flights')], max_length=250)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='co_rolling_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('item_name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full_Name', models.CharField(max_length=250)),
                ('Company', models.CharField(max_length=250)),
                ('Position', models.CharField(max_length=250)),
                ('EMAIL', models.CharField(max_length=250)),
                ('Phone', models.CharField(max_length=250)),
                ('Message', models.CharField(max_length=250)),
            ],
        ),
    ]
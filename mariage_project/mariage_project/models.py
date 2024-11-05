from django.db import models

class in_form(models.Model):
    UN_DB=models.CharField(max_length=200)
    HAP_DB=models.CharField(max_length=200)

class tables(models.Model):
    table_id=models.CharField(max_length=4)
    no_seats=models.CharField(max_length=4)
    setting_name=models.CharField(max_length=250)
    published=models.IntegerField(max_length=1)

class invitees(models.Model):
    name=models.CharField(max_length=200)
    real_name=models.CharField(max_length=200)
    unq_id=models.CharField(max_length=200)
    table_id=models.CharField(max_length=4)
    setting_name=models.CharField(max_length=250)
    e_mail=models.EmailField()
    menu_prefference=models.CharField(max_length=250)
    Freeform_comments=models.CharField(max_length=250)
    particpation=models.CharField(max_length=250)

class invitees_x_table(models.Model):
    name=models.CharField(max_length=200)
    r_name=models.CharField(max_length=200)
    table_id=models.CharField(max_length=4)
    setting_name=models.CharField(max_length=250)


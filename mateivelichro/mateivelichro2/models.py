from django.db import models
from rest_framework import serializers
import datetime
from rest_framework import generics, permissions




class contact(models.Model):

    managed=True
    db_table = "'contact'"
    Full_Name=models.CharField(max_length=250)
    Company=models.CharField(max_length=250)
    Position=models.CharField(max_length=250)
    EMAIL=models.CharField(max_length=250)
    Phone=models.CharField(max_length=250)
    Message=models.CharField(max_length=250)
    

# A item list class for different CO2 generation topics
# Initially this was supposed tobe a key table but Django ORM gives you headaches when it comes to uniquness, not as easy as sql
class co2_items_list(models.Model):
    
    managed=True
    db_table = "'co2_items_list'"
    item_name=models.CharField(max_length=250)
    item_unit=models.CharField(max_length=25)
    item_co2perunit=models.IntegerField()


    
# A table for CO2 generation items. 
# Initially thsese should have been unique but I want to be able to log certain items multipel times so for I'd rather delete 
# and re-insert or simply tolerate multiple entries which are later summed up    
class co2_log(models.Model):

# Restricting entry for previous and current month
    month_choice=(
                  (int(datetime.datetime.now().strftime('%Y%m'))-1,int(datetime.datetime.now().strftime('%Y%m'))-1),
                  (int(datetime.datetime.now().strftime('%Y%m')),int(datetime.datetime.now().strftime('%Y%m'))),
                  )
    
    item_choices=(
        ('LPG','LPG'),
        ('Gasoline', 'Gasoline'),
        ('Elec_ap8','Electricity for ap. 8'),
        ('Elec_ap20','Electricity for ap. 20'),
        ('Gas_ap8','Gas for ap. 8'),
        ('Gas_ap20','Gas for ap. 20'),
        ('Work_flight','Work flights'),
        ('Leisure_flight','Leisure flights')
    )
    
    unit_choice=(('L','Liters'),
                 ('M3','Cubic Meters'),
                 ('KWH','Kilowatt Hours'),
                 ('G','Grams')
                 )
    
    managed=True
    db_table = "'co2_log'"
    month=models.IntegerField(choices=month_choice)
    item_name=models.CharField(max_length=250,choices=item_choices)
    quantity=models.IntegerField()


# A table for CO2 rolling generation items. The previous table simply sums up all the items for a month.
# This table logst total consumption from the begining of time to current month (i.e. 3000 kwh previous month in electricity and this month I have 3200 kwh. This means I used 200kwh of electricity)
# Initially thsese should have been unique but I want to be able to log certain items multipel times so for I'd rather delete and re-insert   
class co_rolling_log(models.Model):
    
    managed=True
    db_table = "'co2_rolling_log'"
    month=models.IntegerField()
    item_name=models.CharField(max_length=250)
    quantity=models.IntegerField()




class co2_log_Serializer(serializers.ModelSerializer):
    class Meta:
        model = co2_log
        fields = '__all__'
        
class co2_rolling_log_Serializer(serializers.ModelSerializer):
    class Meta:
        model = co_rolling_log
        fields = '__all__'

class co2_items_list_Serializer(serializers.ModelSerializer):
    class Meta:
        model = co2_items_list
        fields = '__all__'
        
        

class co2_log_ListView(generics.ListAPIView):
    queryset = co2_log.objects.all()
    serializer_class = co2_log_Serializer
    http_method_names = ['get']
    
class co2_rolling_log_ListView(generics.ListAPIView):
    queryset = co_rolling_log.objects.all()
    serializer_class = co2_rolling_log_Serializer
    http_method_names = ['get']
    
class co2_items_list_ListView(generics.ListAPIView):
    queryset = co2_items_list.objects.all()
    serializer_class = co2_items_list_Serializer
    http_method_names = ['get']
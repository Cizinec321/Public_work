from pickle import FALSE
from django import forms
from django.contrib.auth import get_user_model
from django import forms
from .models import contact, co2_log
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput
from django.forms import ModelForm
import datetime
import base64
from io import StringIO
from django.db.models.fields import BLANK_CHOICE_DASH

#example of superclass
class contact(ModelForm): 




    def __init__(self,*args, **kwargs):     
        super(contact, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form_fields'            
                visible.field.widget.attrs['placeholder']=visible.field.label


        if visible.field.label =='Message':                                
                            visible.field.widget=forms.Textarea()
                            visible.field.widget.attrs['class'] = 'form_fields_l'
                            visible.field.widget.attrs['placeholder']='Leave me a message here.'
    


            

    class Meta:
            model=contact        
            fields = '__all__' 
    


             
class co2_entry(ModelForm): 




    def __init__(self,*args, **kwargs):     
        super(co2_entry, self).__init__(*args, **kwargs)   
        for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form_fields'            
                visible.field.widget.attrs['placeholder']=visible.field.label


            

    class Meta:
            model=co2_log        
            exclude = ('item',)
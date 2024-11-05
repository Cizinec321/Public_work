
from django.contrib.auth import  authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import loginform, registerform, changepwd, m_loginform, m_registerform,m_changepwd,invitees_form,invitees_form_non_su,invitees_form_non_suEN
from django.db.models import Max
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import tables,invitees_x_table, invitees
import os
import string
import random
###################################################################################################################
#                                                                                                                 # 
#                                                                                                                 # 
# This was written while I was learning python and django.                                                        # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
# Allot of it can be refacotred and optimised. I used functions for 'business logic'...etc.                       #
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
# Allot of it can be replaced with javascript.                                                                    #
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
# I now have limited time to do so but I am proud of my first django app so here it is.                           #
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
###################################################################################################################

def seat_generator(topbottom, leftright, seat_per_table):

    height=100/(topbottom)
    widht=70/leftright
    left=0
    top=0
    out_html=''
    if height<widht:
        circleh=height
    else:
        circleh=widht
       
    
    for i in range(leftright):

        top=0
        for z in range(topbottom):
            
            out_html=out_html+'<div style=" display:inline-block;align-items: center;position: relative;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%; aspect-ratio: 1 / 1;border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="submit" name="table_home" value="1" style="background-color: blue;top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;"><input type="hidden" name="id_table" required="" id="id_table" value="'+str(i+1)+str(z+1)+'">'+str(i+1)+str(z+1)+'</button></form></span></div>'
            top=top+height
        left=left+widht
        

    return out_html


#Load seating matrix for Super-User - with editing forms and with data for ALL user's table   
#Make it pretty for HTML display 
def seat_load(name):

    query=tables.objects.filter(setting_name =name) 
    max_val=tables.objects.filter(setting_name =name).aggregate(Max('table_id'))
    
    max_h=int(max_val['table_id__max'][1])
    max_v=int(max_val['table_id__max'][0])  
    height=100/(max_h)
    widht=70/max_v
    left=0
    top=0
    out_html=''
    form_list=[]
    but_count=0
    
    
    for items in query:
          
        if height<widht:
            circleh=height
        else:
            circleh=widht
        
       
        for i in range(max_v):           
            top=0
            for z in range(max_h): 
                #When retrieving invitees list, retrieve invitees for all tables
                inv_list=invitees_x_table.objects.filter(table_id=(str(i+1)+str(z+1)),setting_name=name).values_list('r_name', flat=True)
                str_inv_list=''
                for nm in inv_list:
                    str_inv_list=str_inv_list+nm+'\n'
                data_dict = {'table_id': (str(i+1)+str(z+1)), 'setting_name': name,'assigned_seats':invitees_x_table.objects.filter(table_id=(str(i+1)+str(z+1)),setting_name=name).count(),'already_seated':str_inv_list}                            
                form_list.append(invitees_form(initial=data_dict))
                out_html=out_html+'<div style="display:inline-block;align-items: center;position: relative;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="button" name="table_home" value="1" style="background-color: blue;top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;" onclick=document.getElementById('+chr(39)+str(but_count)+'seating'+chr(39)+').className='+chr(39)+'dropbtn2_show'+chr(39)+'>'+str(but_count+1).zfill(2)+'</button></form></span></div>'
                top=top+height
                but_count=but_count+1
            left=left+widht

        return out_html,form_list
    
#Load seating matrix for non Super-User - without editing forms and with data only for user's table 
#Make it pretty for HTML display    
def seat_load_non_su(unm, lng):
 
    cnt=tables.objects.filter(published=1).count()
    if cnt>0:
        query=tables.objects.filter(published=1) 
        max_val=tables.objects.filter(published=1).aggregate(Max('table_id'))
        name=str(tables.objects.filter(published=1).aggregate(Max('setting_name'))['setting_name__max']) 
        max_h=int(max_val['table_id__max'][1])
        max_v=int(max_val['table_id__max'][0])  
        height=100/(max_h)
        widht=70/max_v
        left=0
        top=0
        out_html=''
        form_list=[]
        but_count=-1
        but_count_orig=0
        real_names=invitees.objects.filter(name__startswith=unm).values_list('real_name',flat=True)
        


        if height<widht:
                circleh=height
        else:
                circleh=widht
            
        for i in range(max_v):         
                top=0
                for z in range(max_h): 
                    #When retrieving invitees list, retrieve only for tables that have someone with user's ID seated at them
                    inv_list=invitees_x_table.objects.filter(table_id=(str(i+1)+str(z+1)),setting_name=name).values_list('r_name', flat=True)
                    str_inv_list=''                    
                    for nm in inv_list:
                        str_inv_list=str_inv_list+nm+'\n'
                    data_dict = {'assigned_seats':invitees_x_table.objects.filter(table_id=(str(i+1)+str(z+1)),setting_name=name).count(),'already_seated':str_inv_list}  
                    if any(nm in str_inv_list for nm in real_names):   
                        if lng=='EN':
                            form_list.append(invitees_form_non_suEN(initial=data_dict))
                        else:
                            form_list.append(invitees_form_non_su(initial=data_dict))
                        but_count=but_count+1
                        out_html=out_html+'<div style="display:inline-block;align-items: center;position: relative;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;  border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="button" name="table_home" value="1" style="background-color: red;top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;" class="table_nu" onclick=document.getElementById('+chr(39)+str(but_count)+'seating'+chr(39)+').className='+chr(39)+'dropbtn2_show'+chr(39)+'>'+str(but_count_orig+1).zfill(2)+'</button></form></span></div>'
                    
                    else:
                        out_html=out_html+'<div style="display:inline-block;align-items: center;position: relative;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;  border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="button" name="table_home" value="1" style="background-color: blue;top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;"  class="table_nu" onclick=document.getElementById().className='+chr(39)+'dropbtn2_show'+chr(39)+'>'+str(but_count_orig+1).zfill(2)+'</button></form></span></div>'
                    but_count_orig=but_count_orig+1
                    top=top+height
                    
                left=left+widht
    else:
        form_list=[]
        if lng=='EN':
            out_html='<div class="pclass"><form method="post"  name="refusal"><p class="smf_pref_lb">A seating plan has not been publishet yet. Please check again later.</p></form></div>'
        else:
            out_html='<div class="pclass"><form method="post"  name="refusal"><p class="smf_pref_lb">Deocamndată nu a fost publicat un plan de așezare. Vă rugăm verificați mai tărziu.</p></form></div>'
    return out_html,form_list



def seat_disp(zname,uname):

    query=tables.objects.filter(setting_name =zname) 
    max_val=tables.objects.filter(setting_name =zname).aggregate(Max('table_id'))
    tbl_list=invitees_x_table.objects.filter(setting_name =zname,name__startswith=uname).values_list('table_id', flat=True)
    
    max_h=int(max_val['table_id__max'][1])
    max_v=int(max_val['table_id__max'][0])  
    height=100/(max_h)
    widht=70/max_v
    left=0
    top=0
    out_html=''
    for items in query:
          
        if height<widht:
            circleh=height
        else:
            circleh=widht
        
        
        for i in range(max_v):

            top=0
            for z in range(max_h):
                if str(i+1)+str(z+1) in tbl_list:
                    
                    clr='red'
                else:
                    clr='blue'
                out_html=out_html+'<div style="display:inline-block;align-items: center;position: relative;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect"  style="top:5px;align-items: center;height:100%; aspect-ratio: 1 / 1;border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="submit" name="table_home" value="1" style="background-color: '+clr+';top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;"><input type="hidden" name="id_table" required="" id="id_table" value="'+str(i+1)+str(z+1)+'">'+str(i+1)+str(z+1)+'</button></form></span></div>'
                top=top+height
            left=left+widht
        

        return out_html
 
 

def m_seat_disp(zname,uname):

    query=tables.objects.filter(setting_name =zname) 
    max_val=tables.objects.filter(setting_name =zname).aggregate(Max('table_id'))
    tbl_list=invitees_x_table.objects.filter(setting_name =zname,name__startswith=uname).values_list('table_id', flat=True)
    
    max_h=int(max_val['table_id__max'][1])
    max_v=int(max_val['table_id__max'][0])  
    height=100/(max_h)
    widht=70/max_v
    left=0
    top=0
    out_html=''
    for items in query:
          
        if height<widht:
            circleh=height
        else:
            circleh=widht
        
        
        for i in range(max_v):

            top=0
            for z in range(max_h):
                if str(i+1)+str(z+1) in tbl_list:
                    
                    clr='red'
                else:
                    clr='black'
                out_html=out_html+'<div style="display:inline-block;align-items: center;position: absolute;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;  border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="submit" name="table_home" value="1" style="background-color: '+clr+';top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;"><input type="hidden" name="id_table" required="" id="id_table" value="'+str(i+1)+str(z+1)+'">'+str(i+1)+str(z+1)+'</button></form></span></div>'
                top=top+height
            left=left+widht
        

        return out_html
 

 
def m_seat_generator(topbottom, leftright, seat_per_table):

    height=100/(topbottom)
    widht=70/leftright
    left=0
    top=0
    out_html=''
    if height<widht:
        circleh=height
    else:
        circleh=widht
       
    
    for i in range(leftright):

        top=0
        for z in range(topbottom):

            out_html=out_html+'<div style="display:inline-block; align-items: center;position: absolute;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;  border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="submit" name="table_home" value="1" style="background-color: blue;   top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;"><input type="hidden" name="id_table" required="" id="id_table" value="'+str(i+1)+str(z+1)+'">'+str(i+1)+str(z+1)+'</button></form></span></div>'
            top=top+height
        left=left+widht
        

    return out_html


def m_seat_load(name):

    query=tables.objects.filter(setting_name =name) 
    max_val=tables.objects.filter(setting_name =name).aggregate(Max('table_id'))
    
    max_h=int(max_val['table_id__max'][1])
    max_v=int(max_val['table_id__max'][0])  
    height=100/(max_h)
    widht=70/max_v
    left=0
    top=0
    out_html=''
    for items in query:
          
        if height<widht:
            circleh=height
        else:
            circleh=widht
        
        
        for i in range(max_v):

            top=0
            for z in range(max_h):

                out_html=out_html+'<div style="display:inline-block;align-items: center;position: absolute;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;top:5%;left:0%;"><span class="table_noselect" style="top:5px;align-items: center;height: 100%;aspect-ratio: 1 / 1;  border-radius: 50%; display: inline-block;position: relative"><form method="post" style="position: absolute;align-items: center;height:'+str(circleh)+ '%;'+' aspect-ratio: 1 / 1;"><button type="submit" name="table_home" value="1" style="background-color: blue;top:'+str((circleh/2)-(circleh/5))+ '%;color: white;border: none;border-radius: 70%;position: relative;padding:5px;font-size: 16px;"><input type="hidden" name="id_table" required="" id="id_table" value="'+str(i+1)+str(z+1)+'">'+str(i+1)+str(z+1)+'</button></form></span></div>'
                top=top+height
            left=left+widht
        

        return out_html
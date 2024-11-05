from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .forms import loginform,registerform,seating_generator,loginformEN
from django.contrib.auth import authenticate, login, get_user_model, logout
from . import gen_dat
from . import seating_algo
from .models import in_form, tables, models, invitees,invitees_x_table
from django.db.models import Max
###################################################################################################################
#                                                                                                                 # 
#                                                                                                                 # 
# This was written while I was learning python and django.                                                        # 
#                                                                                                                 # 
#                                                                                                                 # 
#                                                                                                                 # 
# Allot of it can be refacotred and optimised.                                                                    #
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

def home(request):
        agent = request.META["HTTP_USER_AGENT"]
        #standard form parameters
        register_form=registerform(request.POST or None)
        seating_form=seating_generator(request.POST or None)

        #Get html parameters
        uval=request.GET.get('uval')
        pval=request.GET.get('pval')
        langval=request.GET.get('lang')

        if langval=='EN':
                #standard EN template parameters
                login_form=loginformEN(request.POST or None)
                form_wrapper_start_def='<div class="dropbtn2" id="login"><form method="post"  name="login_request" class="STF"><table style="width:100%">'
                form_wrapper_end_seat_aloc='<tr><th></th><th><button type="submit" class="pos_button2" name="add_participant" value="1">Change</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_seat_gen='<tr><th></th><th><button type="submit" class="pos_button2" name="login_request" value="1">Send</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_not_log='<tr><th></th><th><button type="submit" class="pos_button2" name="login_request" value="1" >Connect</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_non_su_nobutton='<tr><th></th><th></th><td></td></tr></table></form></div>'
                form_wrapper_end_non_su_wbutton='<tr><th></th><th><button type="submit" class="pos_button2" name="add_participant" value="1">Change</button></th><td></td></tr></table></form></div>'
                registerform_wrapper_start_hidden='<div class="dropbtn2" id="register"><form method="post"  name="login_request"><table style="width:100%">'
                registerform_wrapper_start_show='<div class="dropbtn2_show" id="register"><form method="post"  name="login_request"><table style="width:100%">'
                seatingform_wrapper_start_show='<div class="dropbtn2_alt_show" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_hide='<div class="dropbtn2" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_hide_alt='<div class="dropbtn2_alt" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_show_wbutton='<div class="dropbtn2_alt_show" id="seating"><form method="post" style="display:inline-block;"><button type="submit" class="pos_button_unload" value="1">Close</button></form>'
                seatingform_wrapper_end_wbutton='<tr><th></th><th><button type="submit" class="pos_button2" name="seating_request" value="1" >Transmite</button><button type="submit" class="pos_button2" name="publish_request" value="1" >Publish</button></th><td></td></tr></table></form></div>'
                seatingform_wrapper_end_nobutton='<tr><th></th><th></th><td></td></tr></table></form></div>'
        else:
                #standard RO template parameters
                login_form=loginform(request.POST or None)
                form_wrapper_start_def='<div class="dropbtn2" id="login"><form method="post"  name="login_request" class="STF"><table style="width:100%">'
                form_wrapper_end_seat_aloc='<tr><th></th><th><button type="submit" class="pos_button2" name="add_participant" value="1">Schimbă</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_seat_gen='<tr><th></th><th><button type="submit" class="pos_button2" name="login_request" value="1">Transmite</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_not_log='<tr><th></th><th><button type="submit" class="pos_button2" name="login_request" value="1" >Conectare</button></th><td></td></tr></table></form></div>'
                form_wrapper_end_non_su_nobutton='<tr><th></th><th></th><td></td></tr></table></form></div>'
                form_wrapper_end_non_su_wbutton='<tr><th></th><th><button type="submit" class="pos_button2" name="add_participant" value="1">Schimbă</button></th><td></td></tr></table></form></div>'
                registerform_wrapper_start_hidden='<div class="dropbtn2" id="register"><form method="post"  name="login_request"><table style="width:100%">'
                registerform_wrapper_start_show='<div class="dropbtn2_show" id="register"><form method="post"  name="login_request"><table style="width:100%">'
                seatingform_wrapper_start_show='<div class="dropbtn2_alt_show" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_hide='<div class="dropbtn2" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_hide_alt='<div class="dropbtn2_alt" id="seating"><form method="post"  name="seating_request" style="width:100%;height:100%;display:inline-block;"><table style="width:100%">'
                seatingform_wrapper_start_show_wbutton='<div class="dropbtn2_alt_show" id="seating"><form method="post" style="display:inline-block;"><button type="submit" class="pos_button_unload" value="1">Închide</button></form>'
                seatingform_wrapper_end_wbutton='<tr><th></th><th><button type="submit" class="pos_button2" name="seating_request" value="1" >Transmite</button><button type="submit" class="pos_button2" name="publish_request" value="1" >Publică</button></th><td></td></tr></table></form></div>'
                seatingform_wrapper_end_nobutton='<tr><th></th><th></th><td></td></tr></table></form></div>'







        #if password and user value are supplied via URL parameters, then log in user
        if uval!=None and pval!=None:
                user=authenticate(request,username=uval,password=pval)
                #If no user found
                if user==None:
                       return render(request,'landing.html',{'language':langval, #Language parameter that determines how some text is displayed and buttons are named
                                                             'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'), #Language parameter that determines how some text is displayed
                                                             'click_form_login':login_form,#Login form since user is not loged in
                                                             'invitees_handling_form':gen_dat.details_load(),#RSVP form for currently logged in user. Since no user is found, form empty
                                                             'form_wrapper_start':form_wrapper_start_def, #Form wrapper parameters that are varibale depending on language. See above
                                                             'form_wrapper_end':form_wrapper_end_not_log})#Form wrapper parameters that are varibale depending on language See above
                #If user found, same as above + Seating Form
                else:
                        try:
                                login(request,user)
                                #If not super user is loged in then load non-superuser seating form that laods data only for invitees from loged in account  
                                if not request.user.is_superuser:
                                        output_l_non_su=seating_algo.seat_load_non_su(request.user,langval)
                                        seating_table_non_su=output_l_non_su[0]
                                        form_list_non_su=output_l_non_su[1]
                        except:
                                return render(request,'landing.html',{'language':langval,
                                                                      'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),
                                                                      'click_form_login':login_form,
                                                                      'invitees_handling_form':gen_dat.details_load(),#RSVP form for currently logged in user. Since user is found, form contains fields
                                                                      'form_wrapper_start':form_wrapper_start_def,
                                                                      'form_wrapper_end':form_wrapper_end_not_log})



        #If login button is pressed, try loging in. If unsucesfull then return tempalte with notification, otherwise retunr standard tempalte
        #If soccesfull laod same stuff as if loged in via URL parameters (see above)
        if request.POST.get("login_request"):
            if login_form.is_valid():
                username=login_form.cleaned_data['username']
                password=login_form.cleaned_data['password']
                user=authenticate(request,username=username,password=password)
                try:
                        login(request,user)
                except:
                        return render(request,'landing.html',{'language':langval,
                                                              'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),
                                                              'click_form_login':login_form,
                                                              'invitees_handling_form':gen_dat.details_load(),
                                                              'form_wrapper_start':form_wrapper_start_def,
                                                              'form_wrapper_end':form_wrapper_end_not_log})
                
                #if loged user is NOT superuser, in generate seating form without editing options
                if not request.user.is_superuser:
                        
                        output_l_non_su=seating_algo.seat_load_non_su(request.user,langval)
                        seating_table_non_su=output_l_non_su[0]
                        form_list_non_su=output_l_non_su[1]
                        
        #if logout button is pressed, log out
        if request.POST.get("logout_request"):
              logout(request)
        
        #If seating request button is pressed      
        if request.POST.get("seating_request"):
              template=request.POST['template']

              #if a tempalte is selected, i.e. if it's not empty  
              if template!='':
                #Get tempalte name and laod it from DB      
                request.session['template_value'] = template
                output_l=seating_algo.seat_load(template)
                seating_table=output_l[0]
                form_list=output_l[1]
                #If a super user is loged in load, editing forms, otherwise load view forms
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list,
                                                                  'invitees_handling_form':gen_dat.details_load(), #This form contains details of all the users except the admin user
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_register':register_form, #Also load a form that allows the creation of a new user. THis is not laoded in case the admin is not loged in
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_table, #load the table form
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})#Sometimes I load something else here but in this case no
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),  #This form contains details of the loged in user
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_seating':seating_table_non_su,#load the table form with the info of currently loged in users
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})#Sometimes I load something else here but in this case no

              else:
                #If tempalte name is empty, then we generate a new seawting template
                #We name the vertical number of table and then the horizontal number of tables and then we generate vertical no X horizontal No number of tables
                horizontal=request.POST['horizontal']
                vertical=request.POST['vertical']
                no_seats=request.POST['no_seats']
                name=request.POST['name']
                request.session['template_value'] = name
                for i in range(int(horizontal)):
                        for z in range(int(vertical)):
                                tables_inst = tables()
                                tables_inst.table_id = str(i+1)+str(z+1)
                                tables_inst.no_seats = str(no_seats)
                                tables_inst.setting_name = name
                                tables_inst.published=0
                                tables_inst.save()
                output_l=seating_algo.seat_load(name)
                seating_table=output_l[0]
                form_list=output_l[1]
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list,
                                                                  'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_table,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_seating':seating_table_non_su,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})
        #If the publish form button is pressed, we save it and make it the default form that laods when non admin user is loged in
        if request.POST.get("publish_request"):
                template=request.POST['template']
                tables.objects.update(published=0)
                tables.objects.filter(setting_name=template).update(published=1)
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_form,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_hide,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})
                else:

                       return render(request,'landing_log.html',{'language':langval,
                                                                 'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                 'seat_handling_form':form_list_non_su,
                                                                 'click_form_login':login_form,
                                                                 'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                 'form_wrapper_start':form_wrapper_start_def,
                                                                 'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                 'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                 'click_form_seating':seating_table_non_su,
                                                                 'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                 'seatingform_wrapper_start':seatingform_wrapper_start_show,
                                                                 'seatingform_wrapper_end':seatingform_wrapper_end_nobutton})

        #IF add participant button is pressed in the table template
        if request.POST.get('add_participant'):
                #link to used seating template
                template=request.session.get('template_value', None)
                #save party name, basically username for entire party
                part_name=request.POST['name']
                #save assigned table name
                table_id=request.POST['table_id']
                real_party=str(invitees.objects.filter(real_name=part_name).aggregate(Max('real_name'))['real_name__max'])
                #Count how many times this user apears in the assigned tables table
                ass_cnt=invitees_x_table.objects.filter(r_name=part_name,table_id=table_id).count()
                #if count is bigger than 0, user already assigned to this table table - then delete
                if ass_cnt>0:
                        invitees_x_table.objects.filter(r_name=part_name,table_id=table_id).delete()
                else:
                        txi_inst = invitees_x_table()
                        txi_inst.name = part_name
                        txi_inst.r_name = real_party
                        txi_inst.table_id = table_id
                        txi_inst.setting_name = template
                        txi_inst.save()
                output_l=seating_algo.seat_load(template)
                seating_table=output_l[0]
                form_list=output_l[1]
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list,
                                                                  'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_table,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_aloc,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_wbutton,
                                                                  'click_form_seating':seating_table_non_su,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_hidden,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show_wbutton,
                                                                  'seatingform_wrapper_end':'</div>'})

        #IF save participant button is pressed
        if request.POST.get('save_participant'):
                #Generate a random 12 char string that is used as initial password that later can be changed by admin only. 
                #I didn't want users to use own passwords because allot of them expressed fear I might steal passwords and they tend to re-use passwords
                p1=gen_dat.id_generator()
                username=request.POST['username']
                email=request.POST['email']
                party_no=int(request.POST['participants'])
                get_user_model().objects.create_user(username,email,p1)
                #We can defin multiple participants for each user ( for +1, children, etc.)
                #assign default values for each user which he can change later
                if party_no>1:
                        for x in range(1, party_no+1):
                                invitees_inst = invitees()
                                invitees_inst.name = str(username)+'_seat '+str(x)
                                invitees_inst.real_name= str(username)+'_seat '+str(x)
                                invitees_inst.unq_id = str(p1)
                                invitees_inst.table_id = 'Not Assigned'
                                invitees_inst.setting_name = 'Not Assigned'
                                invitees_inst.e_mail = email
                                invitees_inst.menu_prefference='Mănânc orice'
                                invitees_inst.Freeform_comments=''
                                invitees_inst.particpation='Nu'
                                invitees_inst.save()
                else:
                                invitees_inst = invitees()
                                invitees_inst.name = str(username)+'_seat 1'
                                invitees_inst.unq_id = str(p1)
                                invitees_inst.table_id = 'Not Assigned'
                                invitees_inst.setting_name = 'Not Assigned'
                                invitees_inst.e_mail = email
                                invitees_inst.real_name= str(username)+'_seat 1'
                                invitees_inst.menu_prefference='Mănânc orice'
                                invitees_inst.Freeform_comments=''
                                invitees_inst.particpation='Nu'
                                invitees_inst.save()
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_form,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_hide,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_seating':seating_table_non_su,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})

        #IF delete participant button is pressed - delete from various places
        if request.POST.get("delete_participant"):
                User = get_user_model()
                User.objects.filter(username=str(request.POST.get("delete_participant"))).delete()
                invitees.objects.filter(name__startswith=str(request.POST.get("delete_participant"))).delete()
                invitees_x_table.objects.filter(name__startswith=str(request.POST.get("delete_participant"))).delete()
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_form,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_hide,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_seating':seating_table_non_su,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_show,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_nobutton})


        #if someone saves data in the invitees form
        if request.POST.get("inv_save"):
                #If not super-user, relaod forms because theya re not editable and we want to se ethe updated data
                if not request.user.is_superuser:
                        output_l_non_su=seating_algo.seat_load_non_su(request.user,langval)
                        seating_table_non_su=output_l_non_su[0]
                        form_list_non_su=output_l_non_su[1]
                post_data = request.POST

                #Update the invitees table for each invitee in this account
                for i in post_data:
                        if str(i).startswith('Seat_'):
                               invitee=post_data[i]
                               num=int(str(i).replace('Seat_',''))
                               invitees.objects.filter(name=invitee).update(real_name=post_data['Participant_Name_'+str(num)],particpation=post_data['Participation_'+str(num)],e_mail=post_data['Email_Adrress_'+str(num)],menu_prefference=post_data['Menu_prefference_'+str(num)],Freeform_comments=post_data['Freeform_comments_'+str(num)])
                #As above, if is superuser, laod forms for all users with editing options, otherwise laod only for curent user
                if request.user.is_superuser:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load(),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_register':register_form,
                                                                  'click_ee_list':gen_dat.get_party_full(),
                                                                  'click_form_seating':seating_form,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_hide,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})
                else:
                        return render(request,'landing_log.html',{'language':langval,
                                                                  'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),
                                                                  'seat_handling_form':form_list_non_su,
                                                                  'click_form_login':login_form,
                                                                  'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),
                                                                  'form_wrapper_start':form_wrapper_start_def,
                                                                  'form_wrapper_end':form_wrapper_end_seat_gen,
                                                                  'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,
                                                                  'click_form_seating':seating_table_non_su,
                                                                  'registerform_wrapper_start':registerform_wrapper_start_show,
                                                                  'seatingform_wrapper_start':seatingform_wrapper_start_hide_alt,
                                                                  'seatingform_wrapper_end':seatingform_wrapper_end_nobutton})

        if request.user.is_authenticated:

                if request.user.is_superuser:
                        try:
                                return render(request,'landing_log.html',{'language':langval,'click_check_div3':gen_dat.gen_text(langval,'main_hidetxt'),'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load(),'form_wrapper_start':form_wrapper_start_def,'form_wrapper_end':form_wrapper_end_seat_gen,'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,'click_form_register':register_form,'click_ee_list':gen_dat.get_party_full(),'click_form_seating':seating_form,'registerform_wrapper_start':registerform_wrapper_start_hidden,'seatingform_wrapper_start':seatingform_wrapper_start_hide,'seatingform_wrapper_end':seatingform_wrapper_end_wbutton})
                        except:
                                logout(request)
                                return render(request,'landing.html',{'language':langval,'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load(),'form_wrapper_start':form_wrapper_start_def,'form_wrapper_end':form_wrapper_end_not_log})
                
                else:
                        try:
                                return render(request,'landing_log.html',{'language':langval,'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),'seat_handling_form':form_list_non_su,'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load_non_su(request.user,langval),'form_wrapper_start':form_wrapper_start_def,'form_wrapper_end':form_wrapper_end_seat_gen,'form_wrapper_end_non_su':form_wrapper_end_non_su_nobutton,'click_form_seating':seating_table_non_su,'registerform_wrapper_start':registerform_wrapper_start_hidden,'seatingform_wrapper_start':seatingform_wrapper_start_hide_alt,'seatingform_wrapper_end':seatingform_wrapper_end_nobutton})
                        except:
                                logout(request)
                                return render(request,'landing.html',{'language':langval,'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load(),'form_wrapper_start':form_wrapper_start_def,'form_wrapper_end':form_wrapper_end_not_log})

        else:
                return render(request,'landing.html',{'language':langval,'click_check_div3':gen_dat.gen_text(langval,'main_showtxt'),'click_form_login':login_form,'invitees_handling_form':gen_dat.details_load(),'form_wrapper_start':form_wrapper_start_def,'form_wrapper_end':form_wrapper_end_not_log})

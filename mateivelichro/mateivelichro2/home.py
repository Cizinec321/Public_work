from django.shortcuts import render
from . import forms, models
import b_classes
from django.core.mail import send_mail
import requests
import json
import os


#GLOBAL VARIABLES read from os variables as passed parameters
STEAM_KEY= os.environ['STEAM_KEY']
STEAM_ID= os.environ['STEAM_ID']
GITHUB_AUTHORIZATION= os.environ['GITHUB_AUTHORIZATION']
ITEMS_LIST=['LPG','Gasoline','Elec_ap8','Elec_ap20','Gas_ap8','Gas_ap20','Work_flight','Leisure_flight']





# this function reads steam API and returns data in a specific, usable format to print in 
def gen_steam_plate():


    steamuser_payload={
            'key':STEAM_KEY,
            'steamids':STEAM_ID
        }
    
    steamgames_payload={
            'key':STEAM_KEY,
            'steamid':STEAM_ID,
            'format':'json'
        }
        
        
    #If something goes bad, don't show anything from steam
    try:
        #reading player info endpoint
        steam_api_resp=b_classes.req_json('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',payload=steamuser_payload)
        #reading player gaming info endpoint
        steamgame_api_resp=b_classes.req_json('https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',payload=steamgames_payload)
        #saving parsed data
        steamuser=steam_api_resp.json_response
        steamgame=steamgame_api_resp.json_response
        #Saving image URL
        img_src=steamuser['response']['players'][0]['avatarfull']
        #Generating HTML plate for prety display
        steam_txt='<p class="p1l">Steam Handle: <a href="'+steamuser['response']['players'][0]['profileurl']+'">'+steamuser['response']['players'][0]['personaname']+'</a></p><p class="p1l"> Last played: '+steamgame['response']['games'][0]['name']+'</p><p class="p1s">Totaling '+str(steamgame['response']['games'][0]['playtime_2weeks'])+' minutes in the last 2 weeks.</p>'
        out_html='<div class="steam_wrapper"><div class="steam_pic" style="background-image: url('+img_src+');"></div><div class="steam_desc">'+steam_txt
        out_html=out_html+'</div></div>'
    except:
          out_html=''

    return out_html

# this function reads github API and returns data in a specific, usable format to print in 
def gen_github_plate():
    
    github_header={
        'Authorization': f'access_token {GITHUB_AUTHORIZATION}'
    }
    
    #If something goes bad, don't show anything from github    
    try:        
        #reading user info endpoint
        githubuser_api_resp=b_classes.req_json('https://api.github.com/users/cizinec321', header=github_header)
        #reading user's public repos endpoint
        githupublicrepos_api_resp=b_classes.req_json('https://api.github.com/users/Cizinec321/repos', header=github_header)
        #saving parsed data
        githubuser=githubuser_api_resp.json_response
        githupublicrepos=githupublicrepos_api_resp.json_response  
        #Saving image URL      
        img_src=githubuser['avatar_url']
        #Generating HTML plate for prety display
        steam_txt='<p class="p1l">GitHub Handle: <a href="'+githubuser['html_url']+'">'+githubuser['login']+'</a></p><p class="p1l"> Public Repo: '+'<a href="'+githupublicrepos[0]['html_url']+'">'+githupublicrepos[0]['name']+'</a></p><p class="p1s">Last push: '+str(githupublicrepos[0]['pushed_at'])[0:10]+'</p>'
        out_html='<div class="steam_wrapper"><div class="steam_pic" style="background-image: url('+img_src+');"></div><div class="steam_desc">'+steam_txt+'</div></div>'
    except:
          out_html=''

    return out_html



# =============  H  O  M  E  =============  
def home(request):
    agent = request.META["HTTP_USER_AGENT"]
    
    #default to non-mobile
    mobile=False
    comm_content_class='comm-content'
    
    #IF mobile then select special class for better display
    if 'Mobile' in agent: 
          mobile=True
          comm_content_class='m_comm-content'


# =============  Initiating forms  =============
    pers_dat_form=forms.contact(request.POST or None)  
    
    #If logged in as admin, initiate CO2 entry forms, otherwise initiate data from CO2 emission models
    if request.user.is_superuser:
        co2_form=forms.co2_entry(request.POST or None)  
        lpg = ''   
        elec_ap8 = ''
        elec_ap20 = ''
        gas_ap8 = ''
        gas_ap20 = ''
        gasoline=''
        work_flight=''
        leisure_flight=''
    else:
        co2_form=''
        co2_query_inst=models.co2_log.objects.all().values()
        key_query_inst=models.co2_items_list.objects.all().values()
        src_data=b_classes.req_sqlite(co2_query_inst,key_query_inst)
        #geenrate plot here
        lpg = src_data.LPG    
        elec_ap8 = src_data.Elec_ap8  
        elec_ap20 = src_data.Elec_ap20
        gas_ap8 = src_data.Gas_ap8
        gas_ap20 = src_data.Gas_ap20
        gasoline=src_data.Gasoline
        work_flight=src_data.Work_flight
        leisure_flight=src_data.Leisure_flight

# =============  Initiating hobby section  =============    
    steam_plate=gen_steam_plate()
    github_plate=gen_github_plate()
    

    #if a POST method is initiated
    if request.method=='POST':
                    # if register form button is pressed, send me an e-mail with the data
                    if request.POST.get("register_form"):
                        print(pers_dat_form.errors)
                        if pers_dat_form.is_valid():
                            mail_body=''
                            for field in pers_dat_form.fields:
                                    
                                    mail_body=mail_body+str(field)+' : '+str(pers_dat_form.cleaned_data[field])+'''\r\n'''
                            send_mail(
                                        'Message via website',
                                        mail_body,
                                        "velich.eduard@gmail.com",
                                        ["velich.eduard@gmail.com"],
                                        fail_silently=False,
                                        )

                            # If form is valid, return main landing page with a message saying all went well
                            return render(request,'landing_alt.html',{"work_flight":work_flight,"leisure_flight":leisure_flight,"gasoline":gasoline,"lpg" : lpg, "elec_ap8": elec_ap8, "elec_ap20": elec_ap20,'display_trigger_comm':'<div id="comm_div" class="'+comm_content_class+'" style="display:block">','comm_msg':'Thank you! Your message was sent to my inbox. I will reply as soon as possible.','pers_data_form':pers_dat_form,'co2_form':co2_form,'steam_plate':steam_plate,'github_plate':github_plate,'mobile':mobile})
                             
                        else:
                           # If form is NOT valid, return main landing page with a message saying somethign went wrong
                           return render(request,'landing_alt.html',{"work_flight":work_flight,"leisure_flight":leisure_flight,"gasoline":gasoline,"lpg" : lpg, "elec_ap8": elec_ap8, "elec_ap20": elec_ap20,'display_trigger_comm':'<div id="comm_div" class="'+comm_content_class+'" style="display:block">','comm_msg':'Something went wrong. Please check the form and try again.','pers_data_form':pers_dat_form,'co2_form':co2_form,'steam_plate':steam_plate,'github_plate':github_plate,'mobile':mobile})
                    
                    
                    
                    # if register CO button is pressed.....
                    if request.POST.get("co2_form"):

                        if co2_form.is_valid():
                            #If, for the entry month, there are no other entries, generate all entries with 0 (otherwise we break CanvasJS and it won't dispaly anything)
                            if models.co2_log.objects.filter(month=co2_form.cleaned_data['month']).count()==0:                                
                                for item in ITEMS_LIST:
                                    co2_update=models.co2_log()
                                    co2_update.month=co2_form.cleaned_data['month']                                 
                                    co2_update.item_name=item                    
                                    co2_update.quantity=0
                                    co2_update.save()
                                    
                            #If submited Item is in list, it's a rolling entry (I always log total consumption from start of time to current)
                            # This means we need to calculate the difference from previous months for non-rolling table, and we simply log the full entry into the rolling table    
                            if co2_form.cleaned_data['item_name']  in ('Elec_ap8','Elec_ap20','Gas_ap8','Gas_ap20'):
                                models.co_rolling_log.objects.filter(item_name=co2_form.cleaned_data['item_name'],month=co2_form.cleaned_data['month']).delete()
                                co2__rolling_inst=models.co_rolling_log()
                                co2__rolling_inst.month=co2_form.cleaned_data['month']   
                                #If no previous value was found, then default to 0
                                try:                             
                                    prev_rolling_value=models.co_rolling_log.objects.filter(month=int(co2_form.cleaned_data['month'])-1,item_name=co2_form.cleaned_data['item_name']).values_list('quantity', flat=True)[0]
                                except:
                                    prev_rolling_value=0   
                                co2__rolling_inst.item_name=co2_form.cleaned_data['item_name']                        
                                co2__rolling_inst.quantity=co2_form.cleaned_data['quantity']
                                #Save rolling data
                                co2__rolling_inst.save()
                                models.co2_log.objects.filter(item_name=co2_form.cleaned_data['item_name'],month=co2_form.cleaned_data['month']).delete()                                
                                co2_inst=models.co2_log()                                
                                co2_inst.month=co2_form.cleaned_data['month']                                 
                                co2_inst.item_name=co2_form.cleaned_data['item_name']  
                                #Calculate quantity - current value-previosu value                      
                                co2_inst.quantity=int(co2_form.cleaned_data['quantity'])-prev_rolling_value
                                #Save data
                                co2_inst.save()
                            #IF item is not for rolling data, simply record and save entry
                            else:
                                co2_inst=models.co2_log()
                                co2_inst.month=co2_form.cleaned_data['month']                                 
                                co2_inst.item_name=co2_form.cleaned_data['item_name']                        
                                co2_inst.quantity=co2_form.cleaned_data['quantity']
                                co2_inst.save()


    # Generic return
    return render(request,'landing_alt.html',{"work_flight":work_flight,"leisure_flight":leisure_flight,"gasoline":gasoline,"lpg" : lpg, "elec_ap8": elec_ap8, "elec_ap20": elec_ap20, "gas_ap8": gas_ap8, "gas_ap20": gas_ap20,'display_trigger_comm':'<div id="comm_div" class="'+comm_content_class+'" style="display:none">','pers_data_form':pers_dat_form,'co2_form':co2_form,'steam_plate':steam_plate,'github_plate':github_plate,'mobile':mobile})


from .models import in_form, tables, models, invitees,invitees_x_table
from .forms import prefferences
from django.contrib.auth import get_user_model
import random
import string


#Simple text return 
def gen_text(lng, sh):
        if lng=='EN':
            outval='<div class="main_hidetxt" id="aboutus">'\
                    '<p class="pclass"><b>About us</b><br><br>'\
                    'We are Bianca and Matei - or Bia and Matei, Bianca and Edi, Bianca and Eduard. Before we were Bianca and Matei, we were Bianca, HR Team UK advusor and Matei, the guy with the reports, SAP and automatization from BAS. We worked for the same company, same function, sometimes the same floor, but we were far from being in love. On the contrary, Bianca had a deep antipathy mixed with fear for Matei. Around summer 2018, Matei thought that Bianca is a cool gal and, according to him, started flirting. But his efforts were not noticed, because Bianca was busy regulating her blood pressure after every e-mail with grammar mistakes she got from Matei.<br><br>'\
                    'During winter 2018, we started working toghether on a project. Spending allot of time toghether and often the alst desperate people on the 4th floor still working at 7PM, Bianca''s anthypathy and fear transformed into sympathy. When Matei mentioned one of his reccuring nightmare and Bianca noticed it''s the same one as hers, specifically taking a math test, Bianca knew they were supposed to, at least, be friends. After some more weeks, Bianca jokingly told a friend that she will marry Matei if he fixed a tool for her, which he did, thus sealing their fate.<br><br>'\
                    'On December 16th 2018, Bianca texted “LMA și SCM” (Happy birthday) to Matei , and extended their discussions from Skype for Business and Outlook to texting outside working hours. So, the flirting started from both sides, salted with jokes stolen from Sector 7, which worked so well (thanks to our advanced flirting skills), that in February 2019 was still exclusivelly professional, but with allot of laughter thanks to our joke exchanges.<br><br>'\
                    'On 22nd February, Bianca took heart and told Matei she bought him a house warming gift, and Matei took hearth and askedd Bianca out for dinner. We went on our first date on 23rd February, had a good time and knew we would spend the rest of our time toghether. Of course we didn''t tell each other that, so it took one more month untill we told each other we want a relationship.<br><br>'\
                    'We started, then, to build our life as a couple, to love every minute of that process and, of course, love each other.<br><br>'\
                    'We were toghether trough dreams-come-true, job changes, a pandemic, unique experiences, apartment renovations, health challenges, we discovered each other, we overcame obstacles, travelled, ate, laughed, got beaten by Ellie(our pet cat), got cat kisses Ellie(our pet cat), we filled our lives with love and peace. If there is one thing we are certain about, it''s that we want to spend the rest of our live toghether, so we want to become a family in front of God and the law, on 1st of June 2024.<br><br>'\
                    'Because you are a part of our life, we would like you to celebrate with us while we write the next chapters of our lives.<br>'\
                    '</div>'\
                    '<div class="'+str(sh)+'" id="aboutyou">'\
                    '<p class="pclass"><b>About you and your participation</b><br><br>'\
                    "Because we are a organised and tech savy couple, we would appreciate if you could use the form on this website to RSVP, fill in your dietary prefferences and contact details.<br><br>"\
                    "We will start with the religious ceremony on June 1st 2024 02:00PM at the All Saints catholic church in Florești.<br><br>"\
                    "The party will be at Wonderland, Orhideea lounge, starting with 03:30PM.<br><br>"\
                    "Most probably you got a link or a QR code. If you access that link or scan the QR code, you should be loged in with your unique account name and password. If this didn't happen, pelase contact us.<br><br>"\
                    "In the Seating Plan section, once one was finalised and published, you will find the seating plan. The table you were assigned to will have it's number in a red circle. If a seating plan hasn't been published, you will receive a warning message. If this is the case, please be patient and check again later.<br><br>"\
                    "In the participant administration section, you will find the details of your unique account. Here you can confirm the aprticipation of each family member. Also, here you will find a list of participants from your family and will be able to edit their names, dietary restrictions and prefferences, contact details and a comment section. Please use them, we will read all of them."\
                    "</p>"\
                    '</div>'\
                    '<div class="main_hidetxt" id="contact">'\
                    '<p class="pclass"><b>Contact</b><br><br><br>'\
                    "<b>Email:</b> velich.eduard[at]gmail.com<br>"\
                    "<b>Email:</b> bianca.marcoci[at]gmail.com<br>"\
                    '</div>'

        else:
            outval='<div class="main_hidetxt" id="aboutus">'\
                    '<p class="pclass"><b>Despre noi</b><br><br>'\
                    'Suntem Bianca și Matei - sau Bia și Matei, Bianca și Edi, Bianca și Eduard. Înainte să fim Bianca și Matei, eram Bianca, advisorul din HR Team UK și Matei, tipul cu rapoarte, SAP și automatizări din BAS. Lucram la aceeași companie, în aceeași funcțiune, uneori la același etaj, dar eram departe de a fi îndrăgostiți unul de altul. Din contră, Bianca nutrea o profundă antipatie amestecată cu frică față de Matei. Prin vara anului 2018, lui Matei i s-a părut că Bianca e o tipă mișto și, susține el, a început să flirteze cu ea, dar eforturile i-au trecut complet neobservate, căci Bianca era ocupată să își regleze tensiunea la fiecare mail cu erori găsite în sistem, primit de la Matei.<br><br>'\
                    'Pe la începutul iernii 2018, am început să lucrăm împreună la un proiect de automatizare. Petrecând destul de mult împreună și adesea rămânând ultimii disperați de la etajul 4 încă lucrând la ora 19, antipatia și frica Biancăi s-au transformat în simpatie. Când Matei i-a spus Biancăi că unul dintre coșmarurile lui recurente este identic cu al ei, anume test/teza la mate, Bianca a știut că trebuie să fie unul parte din viața ceiluilalt, măcar ca buni prieteni. După alte câteva săptămâni, de altfel, Bianca i-a spus prietenei ei că dacă Matei îi repară ceva la instrumentul de automatizare, se și mărită cu el - Matei a reparat, deci practic soarta a fost pecetluită din acel moment.<br><br>'\
                    'Pe 16 Decembrie 2018, Bianca i-a scris “LMA și SCM” lui Matei pe messenger, și a extins altfel discuțiile noastre de pe Skype for Business și Outlook la messenger în afara orelor de muncă. A început de atunci un flirt din ambele părți, presărat cu glume furate de la Sector 7, care a mers așa de bine (datorită capacității noastre avansate de a flirta), încât în Februarie 2019 relația noastră era în continuare exclusiv profesională, cu multe râsete datorate mesajelor virtuale.<br><br>'\
                    'Pe 22 Februarie, Bianca și-a luat inima în dinți și i-a spus lui Matei că i-a luat un cadou de casă nouă, iar Matei și-a luat și mai mult inima în dinți, și a invitat-o pe Bianca la o cină. Am ieșit pentru prima dată pe 23 Februarie, ne-am simțit foarte bine, și am știut că vrem să ne petrecem restul timpului unul cu celălalt. Desigur că nu ne-am spus asta, așa că a mai durat aproape o lună până ne-am decis să facem pasul important de a avea o relație.<br><br>'\
                    'Am început de atunci să ne clădim viața de cuplu, să iubim fiecare minut din proces, și să ne iubim unul pe celălalt.<br><br>'\
                    'Am fost împreună prin vise împlinite, schimbări de job, pandemie, experiențe unice, finisaje de apartamente, provocări de sănătate fizică și psihică, ne-am descoperit unul pe altul și pe noi înșine, ne-am depășit bariere, am călătorit, am mâncat, am râs, ne-am luat bătaie de la Ellie, am luat pupici de la Ellie, ne-am umplut viața de iubire și liniște interioară. Dacă e un lucru de care suntem siguri, e că vrem să continuăm asta pentru tot restul vieții noastre, așa că ne dorim să devenim o familie și în fața legii și a lui Dumnezeu, în data de 1 Iunie 2024.<br><br>'\
                    'Pentru că sunteți parte din viața noastră, ne dorim să ne fiți alături în această dată, cât și în timp ce scriem noile capitole ale vieții noastre.<br>'\
                    '</div>'\
                    '<div class="'+str(sh)+'" id="aboutyou">'\
                    '<p class="pclass"><b>Despre voi și participarea voastră</b><br><br>'\
                    'Cel mai probabil că ați ajuns până aici prin intermediul unui link, sau al unui cod QR unic, atașate invitației la nuntă – asta înseamnă că ne dorim să vă avem alături de noi în această zi specială!<br><br>'\
                    'Accesarea link-ului sau scanarea codului ar fi trebuit să vă conecteze automat cu un cont dedicat cu nume de utilizator și parolă unice. În cazul în care acest lucru nu s-a întâmplat, sau aveți orice alte dificultăți technice, vă rugăm să ne contactați.<br><br>'\
                    'Pentru că suntem un cuplu ultra conectat la tehnologie și organizat, vă rugăm să folosiți formularul din secțiunea “Administrare Participanți” pentru a ne confirma prezența voastră la nuntă, cât și detalii legate de preferințe alimentare, și mai ales date de contact.<br><br>'\
                    'În secțiunea “Administrare participanți”, veți găsi detaliile contului dumneavoastră unic. Aici puteți confirma participarea fiecărui membru din familie în parte, veți avea posibilitatea să editați numele acestora, restricțiile alimentare, detaliile de contact, și să adăugați comentarii sau mențiuni. Vă rugăm să le folosiți, mai ales dacă aveți restricții alimentare. Le vom citi pe toate.<br><br>'\
                    'Mai târziu, în secțiunea “ Plan de așezare,” odată ce acesta va fi finalizat, veți găsi aranjamentul meselor. Masa la care ați fost așezat va avea numărul colorat cu roșu. Dacă planul de așezare nu a fost publicat, veți întâmpina un mesaj de avertizare. În cazul acesta, vă rugăm să verificați pagina mai târziu.Însă nu vă faceți griji, la intrarea în restaurant vă vor aștepta hostesse, care vă vor ajuta să vă găsiți locul, chiar dacă nu ați reușit să îl identificați pe site :).<br><br>'\
                    '<p class="pclass"><b>Programul</b><br><br>'\
                    "Vom incepe cu cununia religioasă sămbătă, 1 Iunie 2024, ora 14:00 la Biserica Catolică 'Toți Sfinții' din Florești.<br><br>"\
                    "Petrecerea va avea loc la Wonderland, sala Orhideea, începând cu ora 15:30.<br><br>"\
                    "</p>"\
                    '</div>'\
                    '<div class="main_hidetxt" id="contact">'\
                    '<p class="pclass"><b>Contact</b><br><br><br>'\
                    "<b>Email:</b> velich.eduard[at]gmail.com<br>"\
                    "<b>Email:</b> bianca.marcoci[at]gmail.com<br>"\
                    '</div>'
        return outval



#Get all invitees accounts, except for admin, from the source table and format it for pretty html display
def get_party_full():
    User = get_user_model()
    users = User.objects.all()
    outval='<table style="top: 2vh;position: relative; table-layout: fixed ; min-width:886px; padding-bottom: 150px; "><tbody>'
    but_count=0
    for x in  users:
        if str(x.username)!='admin':
            query_res=invitees.objects.filter(name__startswith=str(x.username)).count()
            party_res=invitees.objects.filter(name__startswith=str(x.username),particpation='Da').count()
            outval=outval+'<tr><th style="text-align: left;border-bottom: 1px solid pink;"><label >'+str(x.username)+'</label></th>'+'<th style="text-align: left;border-bottom: 1px solid pink;"><label >'+str(query_res)+' Locuri</label></th>'+'<th style="text-align: left;border-bottom: 1px solid pink;"><label >'+str(party_res)+' Participanți</label></th>'+'<th style="text-align: left;"><form method="post"><button type="submit" name="delete_participant" value="'+str(x.username)+'" class="pos_button2">Șterge</button></form></th>'+'<th style="text-align: left;"><form method="post"><button type="button" name="edit_participant" value="'+str(x.username)+'" class="pos_button2" onclick=document.getElementById('+chr(39)+str(but_count)+'utiz'+chr(39)+').className='+chr(39)+'dropbtn2_show'+chr(39)+';document.getElementById('+chr(39)+'register'+chr(39)+').className='+chr(39)+'dropbtn2'+chr(39)+'>Detalii</button></form></th></tr>'
            but_count=but_count+1
    outval=outval+'</tbody></table>'
    return outval
#Get the invitees of one single account from the source table and format it for pretty html display
def get_party_full_non_su(unm, lang):

    outval='<table style="top: 5%;position: relative; table-layout: fixed ; width: 100%; "><tbody>'
    but_count=0

    if str(unm)!='admin':
            query_res=invitees.objects.filter(name__startswith=str(unm)).count()
            party_res=invitees.objects.filter(name__startswith=str(unm),particpation='Da').count()
            if lang=='EN':
                outval=outval+'<tr><th style="text-align: left, width:auto;"><label ><p class="smf_pref_lb">'+str(unm)+'</p></label></th>'+'<th style="text-align: left, width:30%;"><label ><p class="smf_pref_lb">'+str(query_res)+' Seats</p></label></th>'+'<th style="text-align: left, width:auto;"><form method="post"><button type="button" name="edit_participant" value="'+str(unm)+'" class="pos_button2" onclick=document.getElementById('+chr(39)+str(but_count)+'utiz'+chr(39)+').className='+chr(39)+'dropbtn2_show'+chr(39)+';document.getElementById('+chr(39)+'register'+chr(39)+').className='+chr(39)+'dropbtn2'+chr(39)+'><p class="smf_pref_lb">Details</p></button></form></th></tr>'
            else:
                outval=outval+'<tr><th style="text-align: left, width:auto;"><label ><p class="smf_pref_lb">'+str(unm)+'</P></label></th>'+'<th style="text-align: left, width:30%;"><label ><p class="smf_pref_lb">'+str(query_res)+' Locuri</p></label></th>'+'<th style="text-align: left, width:auto;"><form method="post"><button type="button" name="edit_participant" value="'+str(unm)+'" class="pos_button2" onclick=document.getElementById('+chr(39)+str(but_count)+'utiz'+chr(39)+').className='+chr(39)+'dropbtn2_show'+chr(39)+';document.getElementById('+chr(39)+'register'+chr(39)+').className='+chr(39)+'dropbtn2'+chr(39)+'><p class="smf_pref_lb">Detalii</p></button></form></th></tr>'
            but_count=but_count+1
    outval=outval+'</tbody></table>'
    return outval



#generate the first password
def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Extract all the data of each invitee from the source table for all accounts
def details_load():

    User = get_user_model()
    users = User.objects.all()
    form_list=[]



    for items in users:
        if str(items.get_username())!='admin':
            query_res=invitees.objects.filter(name__startswith=str(items.get_username())+'_seat').count()
            seats_list=[]
            real_name=[]
            mail=[]
            menu_pref=[]
            f_comm=[]
            party=[]
            for x in invitees.objects.filter(name__startswith=str(items.get_username())+'_seat').all():
                seats_list.append(str(x.name))
                real_name.append(str(x.real_name))
                mail.append(str(x.e_mail))
                menu_pref.append(str(x.menu_prefference))
                f_comm.append(str(x.Freeform_comments))
                party.append(str(x.particpation))
            prefferences_inst = prefferences(query_res,seat_no=seats_list,r_name=real_name,email=mail,menu_pref=menu_pref,f_comm=f_comm,party=party)
            form_list.append(prefferences_inst)
    return form_list

#Extract all the data of each invitee from the source table for a single account
def details_load_non_su(unm, lng):

    form_list=[]
    if str(unm)!='admin':
            query_res=invitees.objects.filter(name__startswith=str(unm)+'_seat').count()
            seats_list=[]
            real_name=[]
            menu_pref=[]
            f_comm=[]
            party=[]
            mail=[]
            for x in invitees.objects.filter(name__startswith=str(unm)+'_seat').all():
                seats_list.append(str(x.name))
                real_name.append(str(x.real_name))
                menu_pref.append(str(x.menu_prefference))
                f_comm.append(str(x.Freeform_comments))
                party.append(str(x.particpation))
                mail.append(str(x.e_mail))
            prefferences_inst = prefferences(query_res,seat_no=seats_list,r_name=real_name,email=mail,menu_pref=menu_pref,f_comm=f_comm,party=party,lng=lng)
            form_list.append(prefferences_inst)
    return form_list
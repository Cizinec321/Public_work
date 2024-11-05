from pickle import FALSE
from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

user=get_user_model()

class m_registerform(forms.Form):
    username=forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'style':"right:15%;position:absolute;width:70%;height:40px;border: 2;background: white;outline: 0;top: 40px;font-size: 200%;","Placeholder":"Username"})
    )

    email=forms.EmailField(required=True,
    label='',
        widget=forms.Textarea(attrs={'style':"right:15%;position:absolute;width:70%;height:40px;border: 2;background: white;outline: 0;top: 120px;font-size: 200%","Placeholder":"E-Mail"})
    )
    no_party=forms.EmailField(required=True,
    label='',
        widget=forms.NumberInput(attrs={'style':"right:15%;position:absolute;width:70%;height:40px;border: 2;background: white;outline: 0;top: 120px;font-size: 200%","Placeholder":"Number of expected participants"})
    )

class registerform(forms.Form):

    username=forms.CharField(widget=forms.Textarea(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Utilizator</p>'), label_suffix="")
    email=forms.EmailField(widget=forms.Textarea(attrs={'class':'smf_pref'}),required=True, label=mark_safe('<p class="smf">E-mail</p>'), label_suffix="")
    participants=forms.CharField(widget=forms.NumberInput(attrs={'class':'smf_pref'}), required=True, label=mark_safe('<p class="smf">Participanți</p>'), label_suffix="")

class prefferences (forms.Form):



    def __init__(self, n,seat_no=None,r_name=None,email=None,menu_pref=None,f_comm=None,party=None,lng=None,  *args, **kwargs):

        super(prefferences, self).__init__(*args, **kwargs)
        if lng=='EN':
            CHOICES_MENU =(
            ("Mănânc orice", "I will eat anything"),
            ("Vegan", "Vegan"),
            ("Vegetarian", "Vegetarian"),
            ("Meniu copii", "Children's menu"),
            ("Altele (menționați in comentarii)", "Other (use comment section)"),
            )
            CHOICES_PARTY=(
                ("Da","Yes"),
                ("Nu","No")
            )
        
        else:
            CHOICES_MENU =(
            ("Mănânc orice", "Mănânc orice"),
            ("Vegan", "Vegan"),
            ("Vegetarian", "Vegetarian"),
            ("Meniu copii", "Meniu copii"),
            ("Altele (menționați in comentarii)", "Altele (menționați in comentarii)"),
            )
            CHOICES_PARTY=(
                ("Da","Da"),
                ("Nu","Nu")
            )
        if lng=='EN':
            for i in range(1, n+1):
                self.fields["Seat_%d" % i] = forms.CharField(initial=seat_no[i-1],label=mark_safe('<br><b><p class="smf_pref_lb">Seat %d </p></b>' % i), label_suffix="",widget=forms.Textarea(attrs={'class':'smf_pref_spec'}))
                self.fields["Participant_Name_%d" % i] = forms.CharField(initial=r_name[i-1],label=mark_safe('<p class="smf_pref_lb">Participant name</p>'), label_suffix="",required=True,widget=forms.Textarea(attrs={'class':'smf_pref'}))
                self.fields["Participation_%d" % i] = forms.ChoiceField(initial=party[i-1],label=mark_safe('<p class="smf_pref_lb">RSVP</p>'), label_suffix="",choices = CHOICES_PARTY,widget=forms.Select(attrs={'class':'smf_pref'}))
                self.fields["Email_Adrress_%d" % i] = forms.CharField(initial=email[i-1],label=mark_safe('<p class="smf_pref_lb">E-mail</p>'), label_suffix="",required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))
                self.fields["Menu_prefference_%d" % i] = forms.ChoiceField(initial=menu_pref[i-1],label=mark_safe('<p class="smf_pref_lb">Culinary restrictions</p>'), label_suffix="",choices = CHOICES_MENU,widget=forms.Select(attrs={'class':'smf_pref'}))
                self.fields["Freeform_comments_%d" % i] = forms.CharField(initial=f_comm[i-1],label=mark_safe('<p class="smf_pref_lb">Coments</p>'), label_suffix="",required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))
        else:
            for i in range(1, n+1):
                self.fields["Seat_%d" % i] = forms.CharField(initial=seat_no[i-1],label=mark_safe('<br><b><p class="smf_pref_lb">Locul %d </p></b>' % i), label_suffix="",widget=forms.Textarea(attrs={'class':'smf_pref_spec'}))
                self.fields["Participant_Name_%d" % i] = forms.CharField(initial=r_name[i-1],label=mark_safe('<p class="smf_pref_lb">Nume participant</p>'), label_suffix="",required=True,widget=forms.Textarea(attrs={'class':'smf_pref'}))
                self.fields["Participation_%d" % i] = forms.ChoiceField(initial=party[i-1],label=mark_safe('<p class="smf_pref_lb">Confirmare participare</p>'), label_suffix="",choices = CHOICES_PARTY,widget=forms.Select(attrs={'class':'smf_pref'}))
                self.fields["Email_Adrress_%d" % i] = forms.CharField(initial=email[i-1],label=mark_safe('<p class="smf_pref_lb">Adresă e-mail</p>'), label_suffix="",required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))
                self.fields["Menu_prefference_%d" % i] = forms.ChoiceField(initial=menu_pref[i-1],label=mark_safe('<p class="smf_pref_lb">Restrictii culinare</p>'), label_suffix="",choices = CHOICES_MENU,widget=forms.Select(attrs={'class':'smf_pref'}))
                self.fields["Freeform_comments_%d" % i] = forms.CharField(initial=f_comm[i-1],label=mark_safe('<p class="smf_pref_lb">Comentarii</p>'), label_suffix="",required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))



class m_prefferences (forms.Form):



    def __init__(self, n,seat_no=None,r_name=None,menu_pref=None,f_comm=None,party=None,  *args, **kwargs):

        super(m_prefferences, self).__init__(*args, **kwargs)
        CHOICES_MENU =(
        ("We will eat anything", "We will eat anything"),
        ("No fish", "No fish"),
        ("No meat, no fish", "No meat, no fish"),
        ("No meat", "No meat"),
        ("Children's menu", "Children's menu"),
        ("Other (specify in coments)", "Other (specify in coments)"),
        )
        CHOICES_PARTY=(
            ("Yes","Yes"),
            ("No","No")
        )
        for i in range(1, n+1):
            self.fields["Seat_%d" % i] = forms.CharField(initial=seat_no[i-1],widget=forms.Textarea(attrs={'class':'smf_pref'}))
            self.fields["Participant_Name_%d" % i] = forms.CharField(initial=r_name[i-1],required=True,widget=forms.Textarea(attrs={'class':'smf_pref'}))
            self.fields["Participation_%d" % i] = forms.ChoiceField(initial=party[i-1],choices = CHOICES_PARTY,widget=forms.Select(attrs={'class':'smf_pref'}))
            self.fields["Email_Adrress_%d" % i] = forms.CharField(initial=f_comm[i-1],required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))
            self.fields["Menu_prefference_%d" % i] = forms.ChoiceField(initial=menu_pref[i-1],choices = CHOICES_MENU,widget=forms.Select(attrs={'class':'smf_pref'}))
            self.fields["Freeform_comments_%d" % i] = forms.CharField(initial=f_comm[i-1],required=False,widget=forms.Textarea(attrs={'class':'smf_pref'}))
            

class loginform(forms.Form):
    username=forms.CharField(widget=forms.Textarea(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Nume de utilizator</p>'), label_suffix="")
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Parolă</p>'), label_suffix=""
    )

class loginformEN(forms.Form):
    username=forms.CharField(widget=forms.Textarea(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Username</p>'), label_suffix="")
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Password</p>'), label_suffix=""
    )

class m_loginform(forms.Form):
    username=forms.CharField(label='',
        widget=forms.Textarea(attrs={'style':"right:15%;position:absolute;width:70%;height:60px;border: 2;background: white;outline: 2;top: 40px;font-size: 100%;text-align: center;font-family: Arial, Helvetica, sans-serif;padding-top: 10px;padding-bottom: 10px;","Placeholder":"Username"})
    )
    password=forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'style':"right:15%;position:absolute;width:70%;height:60px;border: 2;background: white;outline: 2;top: 150px;font-size: 100%;text-align: center;font-family: Arial, Helvetica, sans-serif;padding-top: 10px;padding-bottom: 10px;","Placeholder":"Password"})
    )

class changepwd(forms.Form):
    password1=forms.CharField(
        widget=forms.PasswordInput
    )
    password2=forms.CharField(
        widget=forms.PasswordInput
    )
class m_changepwd(forms.Form):
    password1=forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'style':"right:15%;position:absolute;width:70%;height:60px;border: 2;background: white;outline: 0;top: 40px;font-size: 50%","Placeholder":"Type Password"})
    )
    password2=forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'style':"right:15%;position:absolute;width:70%;height:60px;border: 2;background: white;outline: 0;top: 120px;font-size: 50%","Placeholder":"Re-Type Password"})
    )

class input_form(forms.Form):
    #UN=forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols':50, 'style':"left:5%;position:relative;"}), disabled=True)
    HAP=forms.CharField(widget=forms.Textarea(attrs={'style':"left:5%;position:absolute;width:90%;height:50%;border: 2;background: white;outline: 0;bottom: 10vh"}))


class m_input_form(forms.Form):
    #UN=forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols':50, 'style':"left:5%;position:relative;"}), disabled=True)
    HAP=forms.CharField(widget=forms.Textarea(attrs={'style':"left:5%;position:absolute;width:90%;height:20%;border: 2;background: white;outline: 0;bottom: 30vh"}))


class seating_generator(forms.Form):
        vertical=forms.CharField(widget=forms.NumberInput(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Vertical</p>'), label_suffix="", required=False)
        horizontal=forms.CharField(widget=forms.NumberInput(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Horizontal</p>'), label_suffix="", required=False)
        no_seats=forms.CharField(widget=forms.NumberInput(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">No of seats</p>'), label_suffix="", required=False)
        name=forms.CharField(widget=forms.Textarea(attrs={'class':'smf_pref'}),label=mark_safe('<p class="smf">Name</p>'), label_suffix="",required=False)
        template= forms.ModelChoiceField(
        queryset=tables.objects.values_list("setting_name", flat=True).distinct(), required=False, label=mark_safe('<p class="smf">Model</p>'), label_suffix="",widget=forms.Select(attrs={'class':'smf_pref'}),
    )

class m_seating_generator(forms.Form):
        vertical=forms.CharField(widget=forms.NumberInput(attrs={'style':"width:95%;height:100%;font-size: 50%;"}), required=False)
        horizontal=forms.CharField(widget=forms.NumberInput(attrs={'style':"width:95%;height:40%;font-size: 50%;"}), required=False)
        no_seats=forms.CharField(widget=forms.NumberInput(attrs={'style':"width:95%;height:40%;font-size: 50%;"}), required=False)
        name=forms.CharField(required=False)
        template= forms.ModelChoiceField(
        queryset=tables.objects.values_list("setting_name", flat=True).distinct(), required=False
    )


class invitees_form(forms.Form):

    name = forms.ModelChoiceField(invitees.objects.values_list("real_name", flat=True).filter(particpation='Da'), required=False,label=mark_safe('<p class="smf">Participant name</p>'), label_suffix="",widget=forms.Select(attrs={'class':'smf_pref'}))
    table_id=forms.CharField(disabled=False, label=mark_safe('<p class="smf">Table ID</p>'), label_suffix="",widget=forms.Textarea(attrs={'class':'smf_pref'}))
    setting_name=forms.CharField(disabled=True, label=mark_safe('<p class="smf">Model Name</p>'), label_suffix="",widget=forms.Textarea(attrs={'class':'smf_pref'}))
    assigned_seats=forms.CharField(disabled=True,label=mark_safe('<p class="smf">Occupied seats</p>'), label_suffix="",widget=forms.Textarea(attrs={'class':'smf_pref'}))
    already_seated=forms.CharField(widget=forms.Textarea(attrs={'class':'smf'}), label_suffix="",disabled=True, label=mark_safe('<p class="smf">Persoane așezate</p>'))

class invitees_form_non_su(forms.Form):
    assigned_seats=forms.CharField(disabled=True, widget= forms.TextInput(attrs={'class':'smf'}),label=mark_safe('<p class="smf">Locuri ocupate</p>'), label_suffix="")
    already_seated=forms.CharField(widget=forms.Textarea(attrs={'class':'smf'}),disabled=True, label=mark_safe('<p class="smf">Persoane așezate</p>'), label_suffix="")

class invitees_form_non_suEN(forms.Form):
    assigned_seats=forms.CharField(disabled=True, widget= forms.TextInput(attrs={'class':'smf'}),label=mark_safe('<p class="smf">Occupied seats</p>'), label_suffix="")
    already_seated=forms.CharField(widget=forms.Textarea(attrs={'class':'smf'}),disabled=True, label=mark_safe('<p class="smf">Seated participants</p>'), label_suffix="")

class invitees_disp(forms.Form):

    table_id=forms.CharField(disabled=True)
    assigned_seats=forms.CharField(disabled=True)



class m_invitees_disp(forms.Form):

    table_id=forms.CharField( disabled=True)
    assigned_seats=forms.CharField( disabled=True)






    
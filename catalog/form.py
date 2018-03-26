from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from .models import Patient, Appointment,Slots
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm,forms.ModelForm):
    error_css_class='error'
    required_css_class='required'
    '''First_Name=forms.CharField(max_length=40)
    Last_Name=forms.CharField(max_length=40)
    Middle_Name=forms.CharField(max_length=40)
    Address=forms.CharField(max_length=200)
    Date_Of_Birth=forms.DateField()
    Blood_Grp=forms.CharField(max_length=8)
    '''

    class Meta:
        model = User
        fields = ('username',
            'password1',
            'password2'
            )


class apointForm(forms.ModelForm):
    # doctor_name=forms.ChoiceField()
    doctor_name=forms.CharField(required=True, widget=forms.Select(choices=[]))
    slot=forms.CharField(required=True, widget=forms.Select(choices=[]))
    # slot=forms.ChoiceField()
    date=forms.DateField(required=False)

    class Meta:
        model=Appointment
        fields={'doctor_name','slot','date'}
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slot'].queryset = Slots.objects.none()

        if 'slot' in self.data:
            try:
                slot_id = int(self.data.get('slot'))
                self.fields['slot'].queryset = Slots.objects.filter(id=slot_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['slot'].queryset = self.instance.doctor_name.slot_set.order_by('name')


class RegistrationForm2(forms.ModelForm):
    # u_id=RegistrationForm()
    First_Name=forms.CharField(max_length=40)
    Last_Name=forms.CharField(max_length=40)
    Middle_Name=forms.CharField(max_length=40)
    Address=forms.CharField(max_length=200)
    Date_Of_Birth=forms.DateField()
    Blood_Grp=forms.CharField(max_length=8)
    

    class Meta:
        model = Patient
        fields = ('First_Name','Last_Name','Middle_Name','Address','Date_Of_Birth','Blood_Grp')    

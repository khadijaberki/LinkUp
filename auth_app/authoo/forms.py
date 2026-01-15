from django import forms
from .models import Person, Student, Faculty, Campus, Job

class UserProfileForm(forms.ModelForm):
    matricule = forms.CharField(required=False)
    niveau = forms.CharField(required=False)
    poste = forms.CharField(required=False)
    salaire = forms.FloatField(required=False)

    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=False)
    campus = forms.ModelChoiceField(queryset=Campus.objects.all(), required=False)
    job = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)

    class Meta:
        model = Person
        fields = ['username', 'password', 'nom', 'prenom', 'date_naissance', 'tlf']
        widgets = {
            'password': forms.PasswordInput(),
            'date_naissance': forms.DateInput(attrs={'type': 'date'})
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class StudentProfilForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['matricule', 'niveau']



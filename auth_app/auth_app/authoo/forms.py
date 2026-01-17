from django import forms
from django.contrib.auth.models import User
from authoo.models import Etudiant, Employe

# Formulaire pour User (nom d’utilisateur et mot de passe)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

# Formulaire Employé
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'date_naissance', 'tel', 'faculty', 'office', 'job', 'campus']

# Formulaire Étudiant
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'date_naissance', 'tel', 'faculty', 'cursus', 'niveau']

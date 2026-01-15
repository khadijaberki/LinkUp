from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password  # <-- important !
from authoo.models import Employe, Etudiant  # <-- importer les modèles corrects

def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        faculty = request.POST.get('faculty')

        # Création de l'utilisateur Django
        user = User.objects.create(
            username=f"{nom.lower()}.{prenom.lower()}",
            first_name=prenom,
            last_name=nom,
            password=make_password(password)  # hasher le mot de passe
        )

        if role == 'etudiant':
            cursus = request.POST.get('cursus')
            niveau = request.POST.get('niveau')
            Etudiant.objects.create(
                user=user,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                tel=tel,
                faculty=faculty,
                cursus=cursus,
                niveau=niveau
            )
        elif role == 'employe':
            office = request.POST.get('office')
            job = request.POST.get('job')
            campus = request.POST.get('campus')
            Employe.objects.create(
                user=user,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                tel=tel,
                faculty=faculty,
                office=office,
                job=job,
                campus=campus
            )

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')  # rediriger vers la page d'accueil
        else:
            return render(request, 'login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect.'})
    return render(request, 'login.html')


def welcome(request):
    return render(request, 'welcome.html')



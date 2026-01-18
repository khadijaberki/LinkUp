from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from authoo.models import Employe, Etudiant
from .models import Profile, Friend, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q



import random
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from authoo.models import Profile, Etudiant, Employe

def register_view(request):
    error = None

    if request.method == 'POST':
        role = request.POST.get('role')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        faculty = request.POST.get('faculty')
        sexe = request.POST.get('sexe')

        if not role or not nom or not prenom or not date_naissance or not tel or not password or not faculty:
            error = "Veuillez remplir tous les champs obligatoires."
            return render(request, 'register.html', {'error': error})

        # Générer un username simple et unique : nom + prénom
        username = f"{nom.lower()}{prenom.lower()}"
        original_username = username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{count}"
            count += 1

        try:
            # Créer l'utilisateur
            user = User.objects.create(
                username=username,
                first_name=prenom,
                last_name=nom,
                password=make_password(password)
            )

            # Créer profile vide avec tel et statut
            profile = Profile.objects.create(
                user=user,
                tel=tel,
                statut="Étudiant" if role == "etudiant" else "Employé"
            )

            # Créer Etudiant ou Employe
            if role == 'etudiant':
                cursus = request.POST.get('cursus')
                niveau = request.POST.get('niveau')
                if not cursus or not niveau:
                    error = "Veuillez remplir tous les champs étudiant."
                    user.delete()
                    return render(request, 'register.html', {'error': error})

                Etudiant.objects.create(
                    user=user,
                    nom=nom,
                    prenom=prenom,
                    date_naissance=date_naissance,
                    tel=tel,
                    faculty=faculty,
                    sexe=sexe,
                    cursus=cursus,
                    niveau=niveau
                )

            elif role == 'employe':
                office = request.POST.get('office')
                job = request.POST.get('job')
                campus = request.POST.get('campus')
                if not office or not job or not campus:
                    error = "Veuillez remplir tous les champs employé."
                    user.delete()
                    return render(request, 'register.html', {'error': error})

                Employe.objects.create(
                    user=user,
                    nom=nom,
                    prenom=prenom,
                    date_naissance=date_naissance,
                    tel=tel,
                    faculty=faculty,
                    sexe=sexe,
                    office=office,
                    job=job,
                    campus=campus
                )

            # Authentifier et connecter automatiquement
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('welcome')
            else:
                error = "Erreur lors de la connexion automatique."

        except IntegrityError:
            error = "Un problème est survenu. Veuillez réessayer."

    return render(request, 'register.html', {'error': error})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            return render(request, 'login.html', {
                'error': 'Nom d’utilisateur ou mot de passe incorrect.'
            })

    return render(request, 'login.html')


@login_required
def welcome(request):
    user = request.user
    profile_info = ""

    # Profil utilisateur
    try:
        etudiant = Etudiant.objects.get(user=user)
        titre = "Étudiante" if getattr(etudiant, 'sexe', '') == 'F' else "Étudiant"
        profile_info = f"{titre} en {etudiant.niveau} {etudiant.cursus}"
    except Etudiant.DoesNotExist:
        try:
            employe = Employe.objects.get(user=user)
            profile_info = f"Employé - Poste : {employe.job} - Office : {employe.office}"
        except Employe.DoesNotExist:
            pass

    # --- Gestion POST ---
    if request.method == "POST":
        # Ajouter un ami
        friend_id = request.POST.get("add_friend_id")
        if friend_id:
            if int(friend_id) != user.id:
                Friend.objects.get_or_create(user=user, friend_id=int(friend_id))

        # Recherche utilisateur
        keyword = request.POST.get("search")
        search_result = None
        search_msg = ""
        if keyword:
            etu = Etudiant.objects.filter(Q(nom__icontains=keyword) | Q(prenom__icontains=keyword)).first()
            emp = None
            if not etu:
                emp = Employe.objects.filter(Q(nom__icontains=keyword) | Q(prenom__icontains=keyword)).first()

            if etu:
                search_result = {"id": etu.user.id, "nom": etu.nom, "prenom": etu.prenom, "type": "Etudiant"}
            elif emp:
                search_result = {"id": emp.user.id, "nom": emp.nom, "prenom": emp.prenom, "type": "Employe"}
            else:
                search_msg = "Aucun utilisateur trouvé"

        # Publier un message
        content = request.POST.get("message_content")
        if content:
            Message.objects.create(user=user, content=content)

    else:
        search_result = None
        search_msg = ""

    # Liste des amis avec leur type
    friends = Friend.objects.filter(user=user).select_related("friend")
    friends_with_type = []
    for f in friends:
        if Etudiant.objects.filter(user=f.friend).exists():
            f.type = "Etudiant"
        else:
            f.type = "Employe"
        friends_with_type.append(f)

    # Tous les messages
    messages = Message.objects.all().order_by('-created_at')  # dernier message en premier

    context = {
        "friends": friends_with_type,
        "profile_info": profile_info,
        "search_result": search_result,
        "search_msg": search_msg,
        "messages": messages,
    }

    return render(request, "welcome.html", context)


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    statut = profile.statut  # "Étudiant" ou "Employé"
    tel = profile.tel if profile.tel else ""

    context = {
        'profile': profile,
        'nom': user.last_name,
        'prenom': user.first_name,
        'tel': tel,
        'statut': statut,
    }

    return render(request, 'authoo/profile.html', context)



@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    etudiant = Etudiant.objects.filter(user=request.user).first()
    employe = Employe.objects.filter(user=request.user).first()

    if request.method == 'POST':
        request.user.first_name = request.POST.get('prenom')
        request.user.last_name = request.POST.get('nom')
        request.user.save()

        tel = request.POST.get('tel')
        if etudiant:
            etudiant.tel = tel
            etudiant.save()
        elif employe:
            employe.tel = tel
            employe.save()

        profile.bio = request.POST.get('bio')
        profile.statut = request.POST.get('statut')

        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')
       
        profile.tel = tel 

        profile.save()
        return redirect('profile', username=request.user.username)

    context = {
        'profile': profile,
        'nom': request.user.last_name,
        'prenom': request.user.first_name,
        'tel': etudiant.tel if etudiant else employe.tel if employe else '',
        'statut': profile.statut,
 
    }

    return render(request, 'authoo/edit_profile.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_friend(request, user_id):
    if user_id != request.user.id:
        Friend.objects.get_or_create(
            user=request.user,
            friend_id=user_id
        )
    return redirect("welcome")

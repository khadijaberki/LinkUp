from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password  # <-- important !
from authoo.models import Employe, Etudiant  # <-- importer les modèles corrects
from .models import Profile, Friend
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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


#def welcome(request):
    #return render(request, 'welcome.html')
  

def add_friend(request, user_id):
    from django.contrib.auth.models import User
    from .models import Friend
    friend_user = User.objects.get(id=user_id)
    Friend.objects.get_or_create(user=request.user, friend=friend_user)
    return redirect('home')
@login_required
def welcome(request):
    user = request.user
    profile_info = ""

    # Vérifier si étudiant
    try:
        etudiant = Etudiant.objects.get(user=user)
        titre = "Étudiante" if getattr(etudiant, 'sexe', '') == 'F' else "Étudiant"
        profile_info = f"{titre} en {etudiant.niveau} {etudiant.cursus}"
    except Etudiant.DoesNotExist:
        pass

    # Vérifier si employé
    try:
        employe = Employe.objects.get(user=user)
        profile_info = f"Employé - Poste : {employe.job} - Office : {employe.office}"
    except Employe.DoesNotExist:
        pass

    # Liste des amis
    friends = Friend.objects.filter(user=user)

    # IDs de mes amis
    friends_ids = friends.values_list('friend__id', flat=True)

    # Tous les utilisateurs sauf moi et mes amis
    all_users = User.objects.exclude(id__in=friends_ids).exclude(id=user.id)

    # Messages (si tu as un modèle Message)
    # messages = Message.objects.all()
    # form = MessageForm()

    context = {
        'profile_info': profile_info,
        'friends': friends,
        'all_users': all_users,
        # 'messages': messages,
        # 'form': form,
    }

    return render(request, 'welcome.html', context)


#

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    statut = ""
    tel = ""

    try:
        etudiant = Etudiant.objects.get(user=user)
        statut = "Étudiant"
        tel = etudiant.tel
    except Etudiant.DoesNotExist:
        try:
            employe = Employe.objects.get(user=user)
            statut = "Employé"
            tel = employe.tel
        except Employe.DoesNotExist:
            pass

    context = {
        'profile': profile,
        'nom': user.last_name,
        'prenom': user.first_name,
        'tel': tel,
        'statut': statut,
    }

    return render(request, 'authoo/profile.html', context)
    #

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Récupérer étudiant ou employé
    etudiant = Etudiant.objects.filter(user=request.user).first()
    employe = Employe.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # User
        request.user.first_name = request.POST.get('prenom')
        request.user.last_name = request.POST.get('nom')
        request.user.save()

        # Téléphone
        tel = request.POST.get('tel')
        if etudiant:
            etudiant.tel = tel
            etudiant.save()
        elif employe:
            employe.tel = tel
            employe.save()

        # Bio
        profile.bio = request.POST.get('bio')

        # Image
        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')

        profile.save()

        return redirect('profile', username=request.user.username)

    context = {
        'profile': profile,
        'nom': request.user.last_name,
        'prenom': request.user.first_name,
        'tel': etudiant.tel if etudiant else employe.tel if employe else '',
    }

    return render(request, 'authoo/edit_profile.html', context)

@login_required
def add_friend(request, user_id):
    friend_user = get_object_or_404(User, id=user_id)
    # Ajouter l'amitié (à adapter selon ton modèle)
    Friend.objects.get_or_create(user=request.user, friend=friend_user)
    return redirect('welcome')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def add_friend_by_name(request):
    query = request.GET.get('query', '').strip()
    user = request.user
    message = None
    result_user = None

    if query:
        # Chercher par prénom ou nom
        from django.db.models import Q
        result_user = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)).exclude(id=user.id).first()
        if not result_user:
            message = "Aucun utilisateur trouvé"

    context = {
        'result_user': result_user,
        'message': message,
    }
    return render(request, 'authoo/add_friend_by_name.html', context)


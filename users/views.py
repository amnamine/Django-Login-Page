from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import UserScore
from django.db.models import F

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserScore.objects.create(user=user)  # Create score entry for new user
            messages.success(request, f'Account created successfully for {user.username}!')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    user_score, created = UserScore.objects.get_or_create(user=request.user)
    top_scores = UserScore.objects.select_related('user').order_by('-score')[:10]
    return render(request, 'home.html', {
        'user_score': user_score,
        'top_scores': top_scores
    })

@login_required
@require_http_methods(["POST"])
def increment_score(request):
    user_score = UserScore.objects.get(user=request.user)
    user_score.score = F('score') + 1
    user_score.save()
    user_score.refresh_from_db()
    return JsonResponse({'score': user_score.score})

@login_required
def get_leaderboard(request):
    top_scores = UserScore.objects.select_related('user').order_by('-score')[:10]
    leaderboard = [{'username': score.user.username, 'score': score.score} for score in top_scores]
    return JsonResponse(leaderboard, safe=False)

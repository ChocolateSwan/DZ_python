from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate, logout
from django.views import View
from dj_DZ_python.models import *
from django.contrib.auth import login
from dj_DZ_python.forms import *
from dj_DZ_python.paginate import paginate
# Create your views here.


def create_match_view(request, type):
    if not request.user.is_superuser:
        return redirect('MatchModel')

    if request.method == 'POST':
        form = CreateMatchForm(
            request.POST, request.FILES, initial={
                'kind_of_sport': type})
        if form.is_valid():
            match = form.save(True)
            return redirect('match_url', id=match.id)
    else:

        form = CreateMatchForm(initial={'kind_of_sport': type})

    return render(request, 'create_match.html', {
                  'form': form, 'type_of_sport': type})


def create_team_view(request):
    if not request.user.is_superuser:
        return redirect('MatchModel')

    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(True)
            return redirect('MatchModel')
    else:
        form = CreateTeamForm()

    return render(request, 'create_team.html', {'form': form})


# Регистрация
def sign_up(request):
    # При регистрации уже залогиненным редирект на главную
    if request.user.is_authenticated:
        return redirect('MatchModel')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(request.FILES)
            # логиним нового юзера
            auth.login(request, user)
            return redirect('MatchModel')
        return render(request, 'sign_up.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})


# Авторизация
def sign_in(request):
    # При попытке логина уже залогиненным редирект на главную
    if request.user.is_authenticated:
        return redirect('MatchModel')

    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get("username", None),
                                     password=form.cleaned_data.get("password", None))
            if user is not None:  # and user.is_active
                auth.login(request, user)
                return redirect('MatchModel')
            else:
                return render(request, 'sign_in.html', {'form': form})
    else:
        form = AuthorizationForm()
    return render(request, 'sign_in.html', {'form': form})


# Выход
def log_out(request):
    logout(request)
    return redirect('MatchModel')


class MatchListView(View):

    def get(self, request):
        matches = MatchModel.objects.order_by('date_of_match')
        paginated_matches, page_range = paginate(matches, request, 2)
        return render(request, "match_list.html", {
                      "page": paginated_matches, "pageRange": page_range})


class MatchView (LoginRequiredMixin, View):
    login_url = 'sign_in'

    def get(self, request, id):
        match = (MatchModel.objects.filter(id=id))[0]
        antes_part_1 = AnteModel.objects.filter(
            match_for=match.id, team_for=match.participant_1_id)
        antes_part_2 = AnteModel.objects.filter(
            match_for=match.id, team_for=match.participant_2_id)

        form = CreateAnteForm(initial={'match': match,
                                       'antes_part_1': match.participant_1_id,
                                       'antes_part_2': match.participant_2_id})

        return render(request, 'match.html', {"match": match, "form": form, "antes_part_1": antes_part_1,
                                              "antes_part_2": antes_part_2})

    def post(self, request, id):
        match = (MatchModel.objects.filter(id=id))[0]
        antes_part_1 = AnteModel.objects.filter(
            match_for=match.id, team_for=match.participant_1_id)
        antes_part_2 = AnteModel.objects.filter(
            match_for=match.id, team_for=match.participant_2_id)

        form = CreateAnteForm(request.POST, request.FILES, initial={'match': match,
                                                                    'antes_part_1': match.participant_1_id,
                                                                    'antes_part_2': match.participant_2_id})

        if form.is_valid():
            form.save(request.user, match)


        return render(request, 'match.html', {"match": match, "form": form, "antes_part_1": antes_part_1,
                                              "antes_part_2": antes_part_2})

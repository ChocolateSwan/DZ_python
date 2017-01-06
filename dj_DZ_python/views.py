from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dj_DZ_python.models import *
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth import authenticate,logout
from django.views import View
from dj_DZ_python.models import *
from django.contrib.auth import login

# Create your views here.



class CreateMatchForm (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateMatchForm, self).__init__(*args, **kwargs)
        self.fields['participant_1'].queryset = TeamModel.objects.filter(kind_of_sport=self.initial['kind_of_sport'])
        self.fields['participant_2'].queryset = TeamModel.objects.filter(kind_of_sport=self.initial['kind_of_sport'])

    class Meta:
        model = MatchModel
        fields = ('date_of_match','participant_1','participant_2')

    def save(self, commit=False):
        instance = super(CreateMatchForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


def create_match_view(request,type):
    if request.method == 'POST':
        form = CreateMatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(True)
            return redirect('MatchModel')
    else:

        form = CreateMatchForm(initial={'kind_of_sport': type})

    return render(request, 'create_match.html', {'form': form,'type_of_sport':type})






class CreateTeamForm (forms.ModelForm):
    type = forms.ChoiceField(choices=(
                                              ('гандбол', 'гандбол'),
                                              ('баскетбол', 'баскетбол'),
                                              ('волейбол', 'волейбол'),
                                              ('футбол', 'футбол'),
                                              ('бейсбол', 'бейсбол'),),
                                     initial=None,
                                     label='Вид спорта',
                                     required=False)




    def __init__(self, *args, **kwargs):
        super(CreateTeamForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TeamModel
        fields = ('name','rating','quantity_win','quantity_game', 'picture')

    def save(self, commit=False):
        instance = super(CreateTeamForm, self).save(commit=False)
        instance.kind_of_sport = self.cleaned_data['type']
        if commit:
            instance.save()
        return instance


def create_team_view(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(True)
            return redirect('MatchModel')
    else:
        form = CreateTeamForm()

    return render(request, 'create_team.html', {'form': form})





class AuthorizationForm (forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Введите логин', }),
        min_length=5, label='Логин:')
    password = forms.CharField(min_length=8, label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Введите пароль', }))


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Введите логин', }),
        min_length=5, label='Логин:')
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Введите имя', }),
        max_length=30, label='Имя:')
    surname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'surname', 'placeholder': 'Введите фамилию', }),
        max_length=30, label='Фамилия:')
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Введите email', }),
        label="Email")
    password = forms.CharField(min_length=8, label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Введите пароль', }))
    password2 = forms.CharField(min_length=8, label='Повтор пароля:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Повторите пароль', }))
    phone = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Введите номер тел-на'}),
        min_length=11, max_length=11, label='Номер телефона:')
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'id': 'date_of_birth', 'placeholder': "ГГГГ-ММ-ДД"}), label='Дата рождения:')
    date_of_birth = forms.ImageField(
        widget=forms.FileInput(attrs={ 'id': 'avatar'}), label='Аватар:')




    def save(self):
        u = User()
        u.username = self.cleaned_data.get('username')
        u.password = make_password(self.cleaned_data.get('password'))
        u.first_name = self.cleaned_data.get('name')
        u.last_name = self.cleaned_data.get('surname')
        u.email = self.cleaned_data.get('email')
        u.phone = self.cleaned_data('phone')
        u.date_of_birth = self.cleaned_data ('date_of_birth')
        u.avatar = self.cleaned_data ('avatar')
        u.is_staff = False
        u.is_active = True
        u.is_superuser = False
        u.save()

    def clean_password2(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords does not match')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('This login already uses')
        except User.DoesNotExist:
            return username


# Регистрация
def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MatchModel')
        return render(request, 'sign_up.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'sign_up.html', {'form': form})


# Авторизация
def sign_in(request):
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


class MatchListView(View):
    def get(self,request):
        matches = MatchModel.objects.order_by('date_of_match')
        return render(request, "match_list.html", {"matches": matches})


class MatchView (View):
    def get(self, request, id):
        match = (MatchModel.objects.filter(id=id))[0]
        antes_part_1 = AnteModel.objects.filter(match_for=match.id,team_for=match.participant_1_id)
        antes_part_2 = AnteModel.objects.filter(match_for=match.id,team_for=match.participant_2_id)
        return render(request, 'match.html', {"match": match,"antes_part_1": antes_part_1,
                                              "antes_part_2":antes_part_2})
    def post (self, request, id):
        match = (MatchModel.objects.filter(id=id))[0]
        antes_part_1 = AnteModel.objects.filter(match_for=match.id, team_for=match.participant_1_id)
        antes_part_2 = AnteModel.objects.filter(match_for=match.id, team_for=match.participant_2_id)
        return render(request, 'match.html', {"match": match, "antes_part_1": antes_part_1,
                                              "antes_part_2": antes_part_2})





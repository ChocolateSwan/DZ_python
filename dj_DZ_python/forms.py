from dj_DZ_python.models import *
from django import forms
import datetime
from django.db.models import Q


class CreateAnteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateAnteForm, self).__init__(*args, **kwargs)
        self.fields['team_for'].queryset = \
            TeamModel.objects.filter(
            id__in=[
                self.initial['antes_part_1'],
                self.initial['antes_part_2']])
        self.fields['team_for'].empty_label = None

    class Meta:
        model = AnteModel
        fields = ('amount', 'team_for')
        widgets = {
            'amount': forms.TextInput(attrs={'id':'sum_of_ante'}),
            'team_for': forms.RadioSelect(attrs={'id':'participant'})
        }

    def save(self, user, match):
        ante = AnteModel()
        ante.amount = self.cleaned_data.get('amount')
        ante.date_of_ante = datetime.datetime.now()
        ante.team_for = self.cleaned_data.get('team_for')
        ante.match_for = match
        ante.user_for = user
        ante.save()
        return ante


class CreateMatchForm (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateMatchForm, self).__init__(*args, **kwargs)
        self.fields['participant_1'].queryset = TeamModel.objects.filter(
            kind_of_sport=self.initial['kind_of_sport'])
        self.fields['participant_2'].queryset = TeamModel.objects.filter(
            kind_of_sport=self.initial['kind_of_sport'])

    class Meta:
        model = MatchModel
        fields = ('date_of_match', 'participant_1', 'participant_2')
        widgets = {
            'date_of_match': forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder': "ГГГГ-ММ-ДД"})
        }

    def save(self, commit=False):
        instance = super(CreateMatchForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


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
        fields = ('name', 'rating', 'quantity_win', 'quantity_game', 'picture')

    def save(self, commit=False):
        instance = super(CreateTeamForm, self).save(commit=False)
        instance.kind_of_sport = self.cleaned_data['type']
        if commit:
            instance.save()
        return instance


class AuthorizationForm (forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'Введите логин',
            }),
        min_length=5, label='Логин:')
    password = forms.CharField(min_length=8, label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Введите пароль', }))


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'Введите логин',
            }),
        min_length=5, label='Логин:')
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Введите имя',
            }),
        max_length=30, label='Имя:')
    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'surname',
                'placeholder': 'Введите фамилию',
            }),
        max_length=30, label='Фамилия:')
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Введите email',
            }),
        label="Email")
    password = forms.CharField(min_length=8, label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Введите пароль', }))
    password2 = forms.CharField(min_length=8, label='Повтор пароля:', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Повторите пароль', }))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'phone',
                'placeholder': 'Введите номер тел-на'}),
        min_length=11, max_length=11, label='Номер телефона:')
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'id': 'date_of_birth', 'placeholder': "ГГГГ-ММ-ДД"}), label='Дата рождения:')
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'id': 'avatar'}), label='Аватар:', required=False)

    def save(self, files):
        u = User()
        u.username = self.cleaned_data.get('username')
        u.set_password(self.cleaned_data.get('password'))
        u.first_name = self.cleaned_data.get('name')
        u.last_name = self.cleaned_data.get('surname')
        u.email = self.cleaned_data.get('email')
        u.phone = self.cleaned_data.get('phone')
        u.date_of_birth = self.cleaned_data.get('date_of_birth')
        u.avatar = files['avatar']  # self.cleaned_data.get('avatar')
        u.is_staff = False
        u.is_active = True
        u.is_superuser = False
        u.save()
        return u

    def clean_password2(self):
        if self.cleaned_data.get(
                'password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords does not match')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('This login already uses')
        except User.DoesNotExist:
            return username

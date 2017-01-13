from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name='Дата рождения')
    phone = models.CharField(
        max_length=15,
        default='',
        verbose_name='Номер телефона')
    is_in_black_list = models.BooleanField(
        default=0, verbose_name='В черном списке')
    avatar = models.ImageField(
        blank=True,
        max_length=1000,
        verbose_name=u'Аватар')  # upload_to='static/avatar/%Y/%m/'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return str(self.username)


class TeamModel (models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name='Название команды')
    kind_of_sport = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Вид спорта')
    rating = models.IntegerField(default=0, verbose_name='Рэйтинг')
    quantity_win = models.IntegerField(
        default=0, verbose_name='Кол-во выигр. матчей')
    quantity_game = models.IntegerField(
        default=0, verbose_name='Кол-во матчей (всего)')
    picture = models.ImageField(
        blank=True,
        max_length=1000,
        verbose_name='Картинка')

    def __str__(self):
        return str(self.name)


class MatchModel (models.Model):
    date_of_match = models.DateTimeField(
        blank=False, verbose_name='Дата матча')
    participant_1 = models.ForeignKey("TeamModel", null=False, related_name="TeamModel_participant_1",
                                      verbose_name='Участник 1')
    participant_2 = models.ForeignKey("TeamModel", null=False, related_name="TeamModel_participant_2",
                                      verbose_name='Участник 2')

    def __str__(self):
        return str(self.date_of_match)


class AnteModel (models.Model):
    amount = models.FloatField(blank=False, verbose_name="Сумма ставки")
    date_of_ante = models.DateTimeField(verbose_name='Дата ставки')
    user_for = models.ForeignKey(User, null=True, verbose_name='Пользователь')
    team_for = models.ForeignKey(
        "TeamModel",
        null=False,
        verbose_name='Команда')
    match_for = models.ForeignKey(
        "MatchModel", null=False, verbose_name='Матч')

    def __str__(self):
        return str(self.amount)

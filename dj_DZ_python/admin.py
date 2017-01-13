from django.contrib import admin
from .models import *

# Register your models here.


class AnteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'date_of_ante',
        'user_for',
        'team_for',
        'match_for')
    search_fields = ('id', 'amount')

admin.site.register(AnteModel, AnteAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'kind_of_sport',
        'rating',
        'quantity_win',
        'quantity_game',
        'picture')
    list_filter = ['rating']
    search_fields = ('id', 'name')

admin.site.register(TeamModel, TeamAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('date_of_match', 'participant_1', 'participant_2')
    search_fields = ('id', 'date_of_match')

admin.site.register(MatchModel, MatchAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_of_birth', 'phone',
                    'is_in_black_list', 'avatar')

admin.site.register(User, UserAdmin)

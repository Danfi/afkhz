from django.conf.urls import url
from . import views

app_name = 'frontend'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manifest.json$', views.manifest, name='manifest'),
    url(r'^sw.js$', views.sw, name='sw'),
    url(r'^team_compare/$', views.team_compare, name='team_compare'),
    url(r'^data/team_compare/$', views.get_team_compare, name='get_team_compare'),
    url(r'^top30/$', views.top30, name='top30'),
    url(r'^data/top30/$', views.get_top30, name='get_top30'),
    url(r'^newbie/$', views.newbie, name='newbie'),
    url(r'^data/newbie/$', views.get_newbie, name='get_newbie'),
    url(r'^player/$', views.player, name='player'),
    url(r'^data/player/$', views.get_player, name='get_player'),
    url(r'^data/player/list/$', views.get_player_list, name='get_player_list'),
]
from .utils import response_render, get_req_date
from backend.libs.common.utils import get_top_ten_data, get_team_compare_data, get_newbie_data, get_player_data, get_player_list_data
# Create your views here.


@response_render(t='manifest.json', mimetype='application/json; charset=utf-8')
def manifest(request):
    ctx = dict()
    return ctx


@response_render(t='sw.js', mimetype='text/javascript; charset=utf-8')
def sw(request):
    ctx = dict()
    return ctx

    
@response_render(t='index.html')
def index(request):
    ctx = dict()
    return ctx


@response_render(t='team_compare.html')
def team_compare(request):
    ctx = dict()
    return ctx


@response_render
def get_team_compare(request):
    ctx = dict()
    begin_date, end_date = get_req_date(request)
    ctx['json'] = get_team_compare_data(begin_date, end_date)
    return ctx


@response_render(t='top30.html')
def top30(request):
    ctx = dict()
    return ctx


@response_render
def get_top30(request):
    ctx = dict()
    team = request.GET.get('team', 'all')
    if team not in ['all', 'RESISTANCE', 'ENLIGHTENED']:
        team = 'all'
    act = request.GET.get('act', 'all')
    if act not in ['all', 'capture', 'link', 'control_field', 'deploy', 'destroy', 'destroy_link', 'destroy_control_field', 'portal_fracker', 'beacon']:
        act = 'all'
    begin_date, end_date = get_req_date(request)
    ctx['json'] = get_top_ten_data(team, begin_date, end_date, act)
    return ctx


@response_render(t='newbie.html')
def newbie(request):
    ctx = dict()
    return ctx


@response_render
def get_newbie(request):
    ctx = dict()
    begin_date, end_date = get_req_date(request)
    ctx['json'] = get_newbie_data(begin_date, end_date)
    return ctx


@response_render(t='player.html')
def player(request):
    ctx = dict()
    return ctx


@response_render
def get_player(request):
    ctx = dict()
    begin_date, end_date = get_req_date(request)
    ctx['json'] = get_player_data(request.GET.get('player'), begin_date, end_date)
    return ctx


@response_render
def get_player_list(request):
    ctx = dict()
    ctx['json'] = get_player_list_data()
    return ctx

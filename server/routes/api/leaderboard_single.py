from app import app
from flask import jsonify, request
from urllib.request import urlopen, Request
import json

@app.route('/api/leaderboard-single', methods=['GET'])
def leaderboard_single():
  API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords/v2/'
  date = request.args.get('date')

  daily_id_res = urlopen(API_ROOT + '/puzzle/daily-' + date + '.json')
  daily_id_data = daily_id_res.read()
  daily_id = json.loads(daily_id_data)['results'][0]['puzzle_id']

  mini_id_res = urlopen(API_ROOT + '/puzzle/mini-' + date + '.json')
  mini_id_data = mini_id_res.read()
  mini_id = json.loads(mini_id_data)['results'][0]['puzzle_id']

  users = [
    {
      'name': 'Justin',
      'user_cookie': app.config['JM_COOKIE'],
      'daily_results': {},
      'mini_results': {}
    },
    {
      'name': 'Danny',
      'user_cookie': app.config['DIV_COOKIE'],
      'daily_results': {},
      'mini_results': {}
    }
  ]

  for user in users:
    header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
    mini_results_req = urlopen(Request(API_ROOT + 'game/' + str(mini_id) + '.json', headers=header))
    mini_results_res = mini_results_req.read()
    mini_results = json.loads(mini_results_res)['results']

    # TODO: find a game where word/square etc were checked to see if those booleans come through different than "isAutocheckEnabled"
    user['mini_results'] = {
      'isSolved': mini_results.get('solved') or False,
      'solvedAt': mini_results.get('firstSolved') or 0,
      'startedAt': mini_results.get('firstOpened') or 0,
      'completed': mini_results.get('completed') or False,
      'timeElapsed': mini_results.get('timeElapsed') or 0,
      'usedAutoComplete': mini_results.get('isAutocheckEnabled') or False,
    }

    daily_results_req = urlopen(Request(API_ROOT + 'game/' + str(daily_id) + '.json', headers=header))
    daily_results_res = daily_results_req.read()
    daily_results = json.loads(daily_results_res)['results']

    user['daily_results'] = { 
      'isSolved': daily_results.get('solved') or False,
      'solvedAt': daily_results.get('firstSolved') or 0,
      'startedAt': daily_results.get('firstOpened') or 0,
      'completed': daily_results.get('completed') or False,
      'timeElapsed': daily_results.get('timeElapsed') or 0,
      'usedAutoComplete': daily_results.get('isAutocheckEnabled') or False,
    }
    
  response_dict = {
    'status': 'success', # TODO: add failure/error handling
    'message': '',
    'data': users, #TODO: remove user_id and user_cookie from response
  }
    
  return jsonify(response_dict);
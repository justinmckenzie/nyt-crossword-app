from flask import jsonify, request
from app import app
import requests
from datetime import datetime, timedelta

@app.route('/api/leaderboard-single', methods=['GET'])
def leaderboard_single():
  API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords/v2/'

  date = request.args.get('date')

  dailyIdRequest = requests.get(API_ROOT + '/puzzle/daily-' + date + '.json')
  miniIdRequest = requests.get(API_ROOT + '/puzzle/mini-' + date + '.json')
  
  DATE_DAILY_ID = dailyIdRequest.json()['results'][0]['puzzle_id']
  DATE_MINI_ID = miniIdRequest.json()['results'][0]['puzzle_id']

  # Get results for the users
  # TODO: harcoded for now, this will eventually come from the DB once its set up to accept other users
  users = [
    {
      'name': 'Justin',
      'user_id': app.config['JM_ACCT'],
      'user_cookie': app.config['JM_COOKIE'],
      'daily_results': {},
      'mini_results': {}
    },
    {
      'name': 'Danny',
      'user_id': app.config['DIV_ACCT'],
      'user_cookie': app.config['DIV_COOKIE'],
      'daily_results': {},
      'mini_results': {}
    }
  ]

  for user in users:
    header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
    mini_results_req = requests.get(API_ROOT + 'game/' + str(DATE_MINI_ID) + '.json', headers=header)
    mini_results_res = mini_results_req.json()['results']

    # TODO: find a game where word/square etc were checked to see if those booleans come through different than "isAutocheckEnabled"
    user['mini_results'] = {
      'isSolved': mini_results_res.get('solved') or False,
      'solvedAt': mini_results_res.get('firstSolved') or 0,
      'startedAt': mini_results_res.get('firstOpened') or 0,
      'completed': mini_results_res.get('completed') or False,
      'timeElapsed': mini_results_res.get('timeElapsed') or 0,
      'usedAutoComplete': mini_results_res.get('isAutocheckEnabled') or False,
    }

    daily_results_req = requests.get(API_ROOT + 'game/' + str(DATE_DAILY_ID) + '.json', headers=header)
    daily_results_res = daily_results_req.json()['results']

    user['daily_results'] = { 
      'isSolved': daily_results_res.get('solved') or False,
      'solvedAt': daily_results_res.get('firstSolved') or 0,
      'startedAt': daily_results_res.get('firstOpened') or 0,
      'completed': daily_results_res.get('completed') or False,
      'timeElapsed': daily_results_res.get('timeElapsed') or 0,
      'usedAutoComplete': daily_results_res.get('isAutocheckEnabled') or False,
    }

  response_dict = {
    'status': 'success', # TODO: add failure/error handling
    'message': '',
    # TODO: change this field to "data"
    'leaderboard': users, #TODO: remove user_id and user_cookie from response
  }
  
  # TODO proper returning of data to mirror what FE expects
  return jsonify(response_dict)

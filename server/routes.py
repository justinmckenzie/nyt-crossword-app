from flask import jsonify, request
from server import app
import requests
from datetime import datetime, timedelta

JM_ACCT = '204967553';
JM_COOKIE = '1wNioL1ea8qHQkkZLtPolUhgDJOzTHhwdlOT1XnB46mWoufTEd8sYUQJvkWQ6cbExjjOoea6bgYnRxckKfk3fLpyiIRQEg69kRorlMAvj9x6cyn1H0a6xn93xDTQO38FS1^^^^CBQSKQiqzI2gBhCR3o2gBhoSMS2rpRlOzElDbvja07fmLRTiIIGd3mEqAgACGkADLRNq_1_xLLhcwyooQMNclbfuS85XA2vr_FMaoN26476_Ma63QahlVKTds8Xi012n8bEsxVCvkqpjXZPSU7sG'

DIV_ACCT = '205899052';
DIV_COOKIE = '1wtHGL21YZhBpebBxn/MFQARh0ii8n62a8Y/8Tb7tQGPNssbqFsIUnoWHIJcGYpJ1JjOoea6bgYnRxckKfk3fLpACoQGgEgOvMFgI7BDbmwfLMlsFTZdfrZzxDTQO38FS1^^^^CBQSKQiJppigBhD6p5igBhoSMS35H5t53ZNnXZYcJOg0SVg-IKyKl2IqAgACGkDKoo3PDK-EG3KejkisFFewgEa1e4TrPp0bgJIAoiFdD4ILybdyLvAjul03ClqSh-zp7guvG-M2rh02GMldRHcF'

# PUZZLE_INFO = API_ROOT + '/v2/puzzle/daily-2023-02-13.json'
# PUZZLE_INFO = API_ROOT + '/v2/puzzle/puzzles.json'
# SOLVE_INFO = API_ROOT + '/v2/game/20842.json'
# API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords'
# PUZZLE_INFO = API_ROOT + '/v2/puzzle/daily-{date}.json'
# SOLVE_INFO = API_ROOT + '/v2/game/{game_id}.json'
# DATE_FORMAT = '%Y-%m-%d'

# WORDLE = https://www.nytimes.com/svc/games/state/wordle/latest

# FROM REDDIT:
# https://nyt-games-prd.appspot.com/svc/crosswords/v3/<subscription-id>/recent.json
# https://nyt-games-prd.appspot.com/svc/crosswords/v3/<subscription-id>/puzzles.json?publish_type=daily&sort_order=asc&sort_by=print_date&date_start=2010-08-01&date_end=2010-08-31&limit=31

NEW_URL = 'https://nyt-games-prd.appspot.com/svc/crosswords/v3/204967553/puzzles.json?publish_type=mini&date_start='
# NEW_URL = 'https://nyt-games-prd.appspot.com/svc/crosswords/v3/204967553/recent.json'

@app.route('/')
@app.route('/leaderboard', methods=['GET'])

def index():
  date = request.args.get('date')

  # TODO: getting the id's of the game can be done elsewhere or something instead of on every request
  # IDEA: do something ahead of time to get the last 30 days id's or something?
  API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords/v2/'
  MINI_ID_REQ = API_ROOT + '/puzzle/mini-' + date + '.json'
  DAILY_ID_REQ = API_ROOT + '/puzzle/daily-' + date + '.json'

  dailyIdRequest = requests.get(DAILY_ID_REQ)
  miniIdRequest = requests.get(MINI_ID_REQ)
  
  DATE_DAILY_ID = dailyIdRequest.json()['results'][0]['puzzle_id']
  DATE_MINI_ID = miniIdRequest.json()['results'][0]['puzzle_id']

  # Get results for the users
  users = [
    {
      'name': 'Justin',
      'user_id': JM_COOKIE,
      'daily_results': {},
      'mini_results': {}
    },
    {
      'name': 'Danny',
      'user_id': DIV_COOKIE,
      'daily_results': {},
      'mini_results': {}
    }
  ]

# Example Completed Mini Response: {'eligible': False, 'firstOpened': 1677530430, 'firstSolved': 1677530519, 'isPuzzleInfoRead': False, 'lastUpdateTime': 1677530520, 'solved': True, 'completed': True, 'timeElapsed': 71, 'epoch': 1677530438}
# Example Completed Daily Response: { 'eligible': False, 'firstOpened': 1677556895, 'firstSolved': 1677558213, 'isPuzzleInfoRead': False, 'isAutocheckEnabled': True, 'lastUpdateTime': 1677558213, 'solved': True, 'completed': True, 'timeElapsed': 1313, 'firstChecked': 1677558161, 'firstCleared': 1677556979, 'epoch': 1677556898}

  for user in users:
    header = { 'Cookie': 'NYT-S=' + user['user_id'] }
    mini_results_req = requests.get(API_ROOT + 'game/' + str(DATE_MINI_ID) + '.json', headers=header)
    mini_results_res = mini_results_req.json()['results']

    # TODO: find a game where word/square etc were checked to see if those booleans come through different than "isAutocheckEnabled"
    user['mini_results'] = {
      'isSolved': mini_results_res.get('solved') or False,
      'solvedAt': mini_results_res.get('firstSolved') or 0,
      'startedAt': mini_results_res.get('firstOpened') or 0,
      'completed': mini_results_res['completed'] or False,
      # 'timeElapsed': str(timedelta(seconds=mini_results_res['timeElapsed'])),
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
      # 'timeElapsed': str(timedelta(seconds=daily_results_res['timeElapsed'])),
      'timeElapsed': daily_results_res.get('timeElapsed') or 0,
      'usedAutoComplete': daily_results_res.get('isAutocheckEnabled') or False,
    }

  response_dict = {
    'status': 'success',
    'message': '',
    'leaderboard': users, #TODO: remove user_id from response
  }
  
  return jsonify(response_dict)
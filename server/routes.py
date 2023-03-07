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

  # FOR LOCAL DEV 
  # users = [
  #   {
  #     'name': 'Justin',
  #     'user_id': JM_COOKIE,
  #     'daily_results': {'eligible': True, 'id': '204967553-20896', 'isPuzzleInfoRead': False, 'lastUpdateTime': 0, 'solved': False, 'timeElapsed': 0, 'unmerged': True},
  #     'mini_results': {'board': ['|0|0', 'M|0|12', 'O|0|16', 'O|0|21', 'N|0|29', 'P|0|1', 'A|0|12', 'Y|0|34', 'M|0|21', 'E|0|37', 'R|0|1', 'I|0|12', 'V|0|17', 'E|0|21', 'R|0|28', 'O|0|1', 'N|0|13', 'E|0|17', 'N|0|22', 'D|0|41', 'F|0|2', 'E|0|6', 'Y|0|6', '|0|0', '|0|0'], 'eligible': False, 'firstOpened': 1678200722, 'firstSolved': 1678200768, 'id': '204967553-20995', 'isPuzzleInfoRead': False, 'lastUpdateTime': 1678200769, 'solved': True, 'completed': True, 'timeElapsed': 46, 'epoch': 1678200727},
  #   },
  #   {
  #     'name': 'Danny',
  #     'user_id': DIV_COOKIE,
  #     'daily_results': {'board': ['E|1|6870', 'A|1|6870', 'R|1|6870', '|0|0', '|0|0', 'S|1|6870', 'K|1|6870', 'I|1|6870', 'S|1|6870', '|0|0', '|0|0', 'L|3|6870', 'A|1|6870', 'T|1|6870', 'C|1|6870', 'H|1|6870', 'G|1|6870', 'L|1|6870', 'O|1|6870', 'W|1|6870', '|0|0', 'H|1|6870', 'A|1|6870', 'R|1|6870', 'T|1|6870', '|0|121', '|0|0', 'A|3|6870', 'G|1|6870', '|6|6875', '|0|0', 'E|1|6870', 'O|1|6870', 'F|1|6870', 'F|1|6870', 'O|1|6870', '|0|0', 'A|1|6870', 'L|1|6870', 'A|1|6870', 'R|1|6870', '|0|0', '|0|0', 'T|3|6870', 'O|1|6870', 'M|1|6870', 'E|1|6870', 'I|1|6870', 'S|1|6870', 'A|1|6870', 'L|1|6870', 'M|1|6870', 'O|1|6870', 'N|1|6870', '|0|0', 'Q|1|6870', 'U|1|6870', 'I|1|6870', 'E|1|6870', 'T|1|6870', '|0|0', 'E|1|6870', 'R|1|6870', 'R|1|6870', '|0|0', '|0|0', '|0|0', 'B|1|6870', 'I|1|6870', 'G|1|6870', 'L|1|6870', 'I|1|6870', 'T|1|6870', 'T|1|6870', 'L|1|6870', 'E|3|6870', 'L|1|6870', 'I|1|6870', 'E|1|6870', 'S|1|6870', 'E|1|6870', 'R|1|6870', 'S|1|6870', '|0|0', '|0|0', 'H|1|6870', 'O|1|6870', '|0|0', '|0|0', '|0|0', 'M|1|6870', 'A|1|6870', 'A|1|6870', 'M|1|6870', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', 'A|1|6870', 'F|1|6870', 'R|1|6870', 'O|1|6870', 'S|1|6870', '|0|0', 'R|1|6870', 'U|1|6871', 'P|1|6871', 'E|1|6871', 'E|1|6871', 'O|1|6871', 'P|1|6871', 'P|1|6871', 'O|1|6871', 'S|1|6871', 'I|1|6871', 'T|1|6871', 'E|1|6871', 'S|1|6871', 'A|1|6871', 'T|3|6871', 'T|1|6871', 'R|1|6871', 'A|1|6871', 'C|1|6871', 'T|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'O|1|6871', '|0|0', 'S|1|6871', 'C|1|6871', 'O|3|6871', 'U|1|6871', 'R|3|6871', '|0|0', 'A|1|6871', 'L|1|6871', 'O|1|6871', 'T|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'U|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'N|1|6871', 'A|1|6871', 'H|1|6871', '|0|0', 'A|1|6871', 'N|1|6871', 'A|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'R|1|18326', 'I|0|18337', 'G|1|18326', 'H|6|18333', 'T|1|18326', 'A|1|18326', 'W|1|18326', 'A|1|18326', 'Y|1|18326', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', '|0|0', 'B|1|6871', 'A|0|18352', 'L|1|6871', 'O|0|18338', 'O|1|6871', '|0|0', 'L|1|6871', 'L|1|6871', 'A|1|6871', 'M|1|6871', 'A|1|6871', 'S|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'E|1|6871', '|0|0', 'O|3|6871', 'U|3|6871', 'T|1|6871', 'I|3|6871', 'N|3|6871', 'F|1|6871', 'R|1|6871', 'O|1|6871', 'N|1|6871', 'T|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'E|1|6871', '|0|0', 'B|1|6871', 'R|1|6871', 'A|1|6871', 'C|1|6871', 'E|3|6871', '|0|0', 'D|1|6871', 'A|1|6871', 'T|1|6871', 'A|1|6871', '|0|0', '|0|0', '|0|0', '|0|0', 'R|1|6871', '|0|0', '|0|0', 'S|0|18342', 'L|1|6871', 'I|1|6871', '|6|6815', '|0|0', '|0|0', 'N|1|6871', 'I|1|6871', 'X|1|6871'], 'eligible': False, 'firstOpened': 1678193603, 'id': '205899052-20896', 'isPuzzleInfoRead': False, 'lastUpdateTime': 1678211982, 'solved': False, 'timeElapsed': 1229, 'firstChecked': 1678200436, 'epoch': 1678193621},
  #     'mini_results': {'board': ['|0|0', 'M|0|6', 'O|0|70', 'O|0|63', 'N|0|15', 'P|0|29', 'A|0|6', 'Y|0|57', 'M|0|57', 'E|0|15', 'R|0|30', 'I|0|6', 'V|0|100', 'E|0|73', 'R|0|16', 'O|0|31', 'N|0|7', 'E|0|96', 'N|0|94', 'D|0|16', 'F|0|1', 'E|0|2', 'Y|0|2', '|0|0', '|0|0'], 'eligible': False, 'firstOpened': 1678187406, 'firstSolved': 1678187520, 'id': '205899052-20995', 'isPuzzleInfoRead': False, 'lastUpdateTime': 1678187521, 'solved': True, 'completed': True, 'timeElapsed': 114, 'epoch': 1678187420}
  #   }
  # ]

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
      'completed': mini_results_res.get('completed') or False,
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

    # FOR LOCAL DEV
    # user['mini_results'] = {
    #   'isSolved': user['mini_results'].get('solved') or False,
    #   'solvedAt': user['mini_results'].get('firstSolved') or 0,
    #   'startedAt': user['mini_results'].get('firstOpened') or 0,
    #   'completed': user['mini_results'].get('completed') or False,
    #   # 'timeElapsed': str(timedelta(seconds=mini_results_res['timeElapsed'])),
    #   'timeElapsed': user['mini_results'].get('timeElapsed') or 0,
    #   'usedAutoComplete': user['mini_results'].get('isAutocheckEnabled') or False,
    # }

    # user['daily_results'] = { 
    #   'isSolved': user['daily_results'].get('solved') or False,
    #   'solvedAt': user['daily_results'].get('firstSolved') or 0,
    #   'startedAt': user['daily_results'].get('firstOpened') or 0,
    #   'completed': user['daily_results'].get('completed') or False,
    #   # 'timeElapsed': str(timedelta(seconds=daily_results_res['timeElapsed'])),
    #   'timeElapsed': user['daily_results'].get('timeElapsed') or 0,
    #   'usedAutoComplete': user['daily_results'].get('isAutocheckEnabled') or False,
    # }

  response_dict = {
    'status': 'success',
    'message': '',
    'leaderboard': users, #TODO: remove user_id from response
  }
  
  return jsonify(response_dict)
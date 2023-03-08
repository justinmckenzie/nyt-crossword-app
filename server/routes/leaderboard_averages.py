from flask import jsonify, request
from app import app
import requests

@app.route('/leaderboard-averages', methods=['GET'])
def leaderboard_averages():
  # TODO: POC will just get the last 31 days (limit), will eventually move onto being able to take in date ranges
  # users = [
  #   {
  #     'name': 'Justin',
  #     'user_id': app.config['JM_ACCT'],
  #     'user_cookie': app.config['JM_COOKIE'],
  #     'data': {},
  #   },
  #   {
  #     'name': 'Danny',
  #     'user_id': app.config['DIV_ACCT'],
  #     'user_cookie': app.config['DIV_COOKIE'],
  #     'data': {},
  #   }
  # ]

  # for user in users:
  #   header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
  #   puzzles_req = requests.get('https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user['user_id'] + '/puzzles.json?publish_type=mini&sort_order=desc&sort_by=print_date', headers=header)
  #   puzzles_res = puzzles_req.json()['results']

  #   in_progress = 0
  #   not_started = 0
  #   solvedIds = []
  #   solveTimes = []

  #   for puzzle in puzzles_res:
  #     if (puzzle['solved'] == True):
  #       solvedIds.append(puzzle['puzzle_id'])
  #     elif (puzzle['percent_filled'] == 0):
  #       not_started = not_started + 1
  #     else:
  #       in_progress = in_progress + 1

  #   for _id in solvedIds: 
  #     mini_req = requests.get('https://nyt-games-prd.appspot.com/svc/crosswords/v2/game/' + str(_id) + '.json', headers=header)
  #     mini_res = mini_req.json()['results']['timeElapsed']
  #     solveTimes.append(mini_res)

  #   user['data'] = {
  #     'completed': len(solvedIds),
  #     'in_progress': in_progress,
  #     'not_started': not_started,
  #     'average': round(sum(solveTimes) / len(solveTimes)),
  #   }

  users = [{'name': 'Justin', 'user_id': '204967553', 'user_cookie': '1wNioL1ea8qHQkkZLtPolUhgDJOzTHhwdlOT1XnB46mWoufTEd8sYUQJvkWQ6cbExjjOoea6bgYnRxckKfk3fLpyiIRQEg69kRorlMAvj9x6cyn1H0a6xn93xDTQO38FS1^^^^CBQSKQiqzI2gBhCR3o2gBhoSMS2rpRlOzElDbvja07fmLRTiIIGd3mEqAgACGkADLRNq_1_xLLhcwyooQMNclbfuS85XA2vr_FMaoN26476_Ma63QahlVKTds8Xi012n8bEsxVCvkqpjXZPSU7sG', 'data': {'completed': 30, 'in_progress': 1, 'not_started': 0, 'average': 88}}, {'name': 'Danny', 'user_id': '205899052', 'user_cookie': '1wtHGL21YZhBpebBxn/MFQARh0ii8n62a8Y/8Tb7tQGPNssbqFsIUnoWHIJcGYpJ1JjOoea6bgYnRxckKfk3fLpACoQGgEgOvMFgI7BDbmwfLMlsFTZdfrZzxDTQO38FS1^^^^CBQSKQiJppigBhD6p5igBhoSMS35H5t53ZNnXZYcJOg0SVg-IKyKl2IqAgACGkDKoo3PDK-EG3KejkisFFewgEa1e4TrPp0bgJIAoiFdD4ILybdyLvAjul03ClqSh-zp7guvG-M2rh02GMldRHcF', 'data': {'completed': 30, 'in_progress': 1, 'not_started': 0, 'average': 65}}]

  return jsonify({ 'data': users })

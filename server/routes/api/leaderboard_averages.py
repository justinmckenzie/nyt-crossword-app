from app import app
from flask import jsonify
from urllib.request import urlopen, Request
import json

@app.route('/api/leaderboard-averages', methods=['GET'])
def leaderboard_averages():
	users = [
		{
			'name': 'Justin',
			'user_id': app.config['JM_ACCT'],
      'user_cookie': app.config['JM_COOKIE'],
			'data': {},
		},
		{
			'name': 'Danny',
      'user_id': app.config['DIV_ACCT'],
      'user_cookie': app.config['DIV_COOKIE'],
			'data': {},
		}
	]

	for user in users:
		header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
		puzzles_req = urlopen(Request('https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user['user_id'] + '/puzzles.json?publish_type=mini&sort_order=desc&sort_by=print_date', headers=header))
		puzzles_res = puzzles_req.read()
		puzzle_data = json.loads(puzzles_res)['results']

		in_progress = 0
		not_started = 0
		solvedIds = []
		solveTimes = []

		for puzzle in puzzle_data:
			if (puzzle['solved'] == True):
				solvedIds.append(puzzle['puzzle_id'])
			elif (puzzle['percent_filled'] == 0):
				not_started = not_started + 1
			else:
				in_progress = in_progress + 1

		for _id in solvedIds: 
			mini_req = urlopen(Request('https://nyt-games-prd.appspot.com/svc/crosswords/v2/game/' + str(_id) + '.json', headers=header))
			mini_res = mini_req.read()
			puzzle_data = json.loads(mini_res)['results']['timeElapsed']
			solveTimes.append(puzzle_data)

		user['data'] = {
			'completed': len(solvedIds),
			'in_progress': in_progress,
			'not_started': not_started,
			'average': round(sum(solveTimes) / len(solveTimes)),
		}

		response_dict = {
			'status': 'success', # TODO: add failure/error handling
			'message': '',
			'data': users, #TODO: remove user_id and user_cookie from response
		}

	return jsonify(response_dict)

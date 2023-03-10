from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request, json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

JM_ACCT = '204967553'
DIV_ACCT = '205899052'
JM_COOKIE = '1wNioL1ea8qHQkkZLtPolUhgDJOzTHhwdlOT1XnB46mWoufTEd8sYUQJvkWQ6cbExjjOoea6bgYnRxckKfk3fLpyiIRQEg69kRorlMAvj9x6cyn1H0a6xn93xDTQO38FS1^^^^CBQSKQiqzI2gBhCR3o2gBhoSMS2rpRlOzElDbvja07fmLRTiIIGd3mEqAgACGkADLRNq_1_xLLhcwyooQMNclbfuS85XA2vr_FMaoN26476_Ma63QahlVKTds8Xi012n8bEsxVCvkqpjXZPSU7sG'
DIV_COOKIE = '1wtHGL21YZhBpebBxn/MFQARh0ii8n62a8Y/8Tb7tQGPNssbqFsIUnoWHIJcGYpJ1JjOoea6bgYnRxckKfk3fLpACoQGgEgOvMFgI7BDbmwfLMlsFTZdfrZzxDTQO38FS1^^^^CBQSKQiJppigBhD6p5igBhoSMS35H5t53ZNnXZYcJOg0SVg-IKyKl2IqAgACGkDKoo3PDK-EG3KejkisFFewgEa1e4TrPp0bgJIAoiFdD4ILybdyLvAjul03ClqSh-zp7guvG-M2rh02GMldRHcF'

@app.route('/ping', methods=['GET'])
def ping_pong():
  return jsonify('pong!')

@app.route('/api/leaderboard-single', methods=['GET'])
def leaderboard_single():
    API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords/v2/'
    date = request.args.get('date')

    daily_id_res = urllib.request.urlopen(API_ROOT + '/puzzle/daily-' + date + '.json')
    daily_id_data = daily_id_res.read()
    daily_id = json.loads(daily_id_data)['results'][0]['puzzle_id']

    mini_id_res = urllib.request.urlopen(API_ROOT + '/puzzle/mini-' + date + '.json')
    mini_id_data = mini_id_res.read()
    mini_id = json.loads(mini_id_data)['results'][0]['puzzle_id']

    users = [
        {
            'name': 'Justin',
            # 'user_id': app.config['JM_ACCT'],
            # 'user_cookie': app.config['JM_COOKIE'],
            'user_cookie': JM_COOKIE,
            'daily_results': {},
            'mini_results': {}
        },
        {
            'name': 'Danny',
            # 'user_id': app.config['DIV_ACCT'],
            # 'user_cookie': app.config['DIV_COOKIE'],
            'user_cookie': DIV_COOKIE,
            'daily_results': {},
            'mini_results': {}
        }
    ]

    for user in users:
        header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
        mini_results_req = urllib.request.urlopen(urllib.request.Request(API_ROOT + 'game/' + str(mini_id) + '.json', headers=header))
        mini_results_res = mini_results_req.read()
        mini_results = json.loads(mini_results_res)['results']

        print('mini results', mini_results)

        # TODO: find a game where word/square etc were checked to see if those booleans come through different than "isAutocheckEnabled"
        user['mini_results'] = {
            'isSolved': mini_results.get('solved') or False,
            'solvedAt': mini_results.get('firstSolved') or 0,
            'startedAt': mini_results.get('firstOpened') or 0,
            'completed': mini_results.get('completed') or False,
            'timeElapsed': mini_results.get('timeElapsed') or 0,
            'usedAutoComplete': mini_results.get('isAutocheckEnabled') or False,
        }

        daily_results_req = urllib.request.urlopen(urllib.request.Request(API_ROOT + 'game/' + str(daily_id) + '.json', headers=header))
        daily_results_res = daily_results_req.read()
        daily_results = json.loads(daily_results_res)['results']

        print(daily_results)

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
        # TODO: change this field to "data"
        'leaderboard': users, #TODO: remove user_id and user_cookie from response
    }
    
    return jsonify(response_dict);

@app.route('/api/leaderboard-averages', methods=['GET'])
def leaderboard_averages():
	print('called')
	# TODO: POC will just get the last 31 days (limit), will eventually move onto being able to take in date ranges
	users = [
		{
			'name': 'Justin',
			'user_id': JM_ACCT,
			'user_cookie': JM_COOKIE,
			'data': {},
		},
		{
			'name': 'Danny',
			'user_id': DIV_ACCT,
			'user_cookie': DIV_COOKIE,
			'data': {},
		}
	]

	for user in users:
		header = { 'Cookie': 'NYT-S=' + user['user_cookie'] }
		puzzles_req = urllib.request.urlopen(urllib.request.Request('https://nyt-games-prd.appspot.com/svc/crosswords/v3/' + user['user_id'] + '/puzzles.json?publish_type=mini&sort_order=desc&sort_by=print_date', headers=header))
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
			mini_req = urllib.request.urlopen(urllib.request.Request('https://nyt-games-prd.appspot.com/svc/crosswords/v2/game/' + str(_id) + '.json', headers=header))
			mini_res = mini_req.read()
			puzzle_data = json.loads(mini_res)['results']['timeElapsed']
			solveTimes.append(puzzle_data)

		user['data'] = {
			'completed': len(solvedIds),
			'in_progress': in_progress,
			'not_started': not_started,
			'average': round(sum(solveTimes) / len(solveTimes)),
		}

		print('users', users)

		response_dict = {
			'status': 'success', # TODO: add failure/error handling
			'message': '',
			# TODO: change this field to "data"
			'leaderboard': users, #TODO: remove user_id and user_cookie from response
		}

	# TODO proper returning of data to mirror what FE expects
	return jsonify(response_dict)


if __name__ == '__main__':
    app.run()

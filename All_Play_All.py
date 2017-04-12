import numpy
import random
import math
from collections import Counter
import scipy
from scipy import optimize
import copy
import Single_Game

# quick summary:
# every team plays every other team n times (n typically 1);
# win = 3 points,
# draw = 1 point,
# loss = 0 point

# test team-payroll dictionary
teams_payroll = {}
teams_payroll['team1'] = 4
teams_payroll['team2'] = 8
teams_payroll['team3'] = 12
teams_payroll['team4'] = 16
teams_payroll['team5'] = 14
teams_payroll['team6'] = 16
teams_payroll['team7'] = 16
teams_payroll['team8'] = 16
teams_payroll['team9'] = 16
teams_payroll['team10'] = 16
teams_payroll['team11'] = 16
teams_payroll['team12'] = 16
teams_payroll['team13'] = 16
teams_payroll['team14'] = 16
teams_payroll['team15'] = 16
teams_payroll['team16'] = 16
teams_payroll['team17'] = 133
teams_payroll['team18'] = 150
teams_payroll['team19'] = 100
teams_payroll['team20'] = 200

# test team-points dictionary
team_points = copy.deepcopy(teams_payroll)
for i in range(0, len(team_points)):
    team_points[team_points.keys()[i]] = 0

# n-round round-robin tournament
# (eg, premier league used n = 2)
def give_points(result, points_dict, team_home, team_away):
    if result == 1:
        points_dict[team_home] += 3
    if result == 2:
        points_dict[team_away] += 3
    if result == 0:
        points_dict[team_home] += 1
        points_dict[team_away] += 1


def n_round_robin(payroll_dict, points_dict, var_pow, draw_window, n):
    n_games = 0
    for i in range(0, n):
        # make everyone play everyone else once
        team_subset = copy.deepcopy(payroll_dict)
        for team_home in payroll_dict:

            # remove home team from subset
            del team_subset[team_home]

            # play everyone in that dict, score points from results
            for team_away in team_subset:

                result = Single_Game.simulate_game(payroll_dict, team_home, team_away, var_pow, draw_window)
                n_games += 1
                give_points(result, points_dict, team_home, team_away)
    #print('num games:', n_games)


def all_play_random(payroll_dict, points_dict, var_pow, draw_window, n):

    n_games = 0
    # copy payroll dict into list
    payroll_list = list()
    for key, value in payroll_dict.iteritems():
        temp = [key, value]
        payroll_list.append(temp)

    # repeat entire process n times
    for i in range(0, n):
        # make everyone play everyone else once

        for team_home in payroll_dict:
            team_subset = copy.deepcopy(payroll_dict)
            # remove home team from subset
            del team_subset[team_home]

            # play a random person in that dict, score points from results, do (n-1) times for n teams
            for j in range(0, len(team_subset)):
                random_away_team = random.choice(team_subset.keys())
                result = Single_Game.simulate_game(payroll_dict, team_home, random_away_team, var_pow, draw_window)
                n_games += 1
                give_points(result, points_dict, team_home, random_away_team)
    #print('num games:', n_games)

if __name__ == "__main__":

    all_play_random(teams_payroll, team_points, 0.0, 0.0, 1)
    n_round_robin(teams_payroll, team_points, 0.0, 0.0, 2)

"""

n_round_robin(teams_payroll, team_points, 500)

print(team_points)

"""
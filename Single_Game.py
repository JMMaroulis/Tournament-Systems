import numpy
import random
import math
from collections import Counter
import scipy
from scipy import optimize


# Intention: Simulate a single game of football

# define various necessaries
team1_list = list()
team2_list = list()
wins_list = list()


# generates a random number for a team based on input payroll
# THIS IS THE BIT THAT'S GOING TO NEED ALL THE WORK
def generate_performance(payroll, var):
    z = numpy.random.normal(payroll, var)
    return z


# method to simulate one game
# returns 1 if team 1 wins, 2 if team 2 wins, 0 if draw
def simulate_game(teams_dict, team1, team2, var_pow, draw_window):

    var = ((teams_dict[team1] + teams_dict[team2]) * 0.5) * var_pow
    a = generate_performance(teams_dict[team1], var)
    b = generate_performance(teams_dict[team2], var)
    draw_margin = ((teams_dict[team1] + teams_dict[team2]) * 0.5) * draw_window

    # if sufficiently close, draw
    if abs(a-b) <= draw_margin:
        return 0
    # if a is sufficiently larger than b, team 1 wins
    elif a >= b:
        return 1
    # if b is sufficiently larger than a, team 2 wins
    elif b >= a:
        return 2


# Error_1 = (LV%_actual - LV_%predicted)^2
# Error_2 = (MU%_actual - MU%_predicted)^2
# Error_3 = (Draw%_actual - Draw%_predicted)^2
def squared_error_metric(team1_actual_percent, team2_actual_percent, draw_actual_percent, results_list):

    # parse results from list
    team1_wins = results_list.count(1)
    team2_wins = results_list.count(2)
    draws = results_list.count(0)
    games = float(len(results_list))

    # turn into percentages
    team1_percent = (team1_wins / games) * 100
    team2_percent = (team2_wins / games) * 100
    draw_percent = (draws / games) * 100
    print (team1_percent, team2_percent, draw_percent)

    # turn into errors
    team1_error = abs(team1_actual_percent - team1_percent)**2.0
    team2_error = abs(team2_actual_percent - team2_percent)**2.0
    draw_error = abs(draw_actual_percent - draw_percent)**2.0

    return team1_error, team2_error, draw_error

"""
# DEFINITIONS OVER, TESTING STARTING
# team dictionary for testing
teams = {}
teams['Team_1'] = float(115.57 * (10**6))
teams['Team_2'] = float(91.71 * (10**6))


for i in range(0, 10**5):
    #variance = 1.1001093047110022
    #draw_mar = 5.0002079619335138
    variance = 1.0
    draw_mar = 5.0
    z = simulate_game(teams, 'Team_1', 'Team_2', variance, draw_mar)
    wins_list.append(z)

# write to file for plotting

# declare files
team_scores = open("team_scores.txt", "w")

for count in range(0, len(team1_list)):
    x = team1_list[count]
    y = team2_list[count]
    team_scores.write('%s' % x)
    team_scores.write(' %s' % y)
    team_scores.write(' %s\n' % count)

# enumerate wins for each team
print(Counter(wins_list))

e1, e2, e3 = squared_error_metric(33.1, 38.5, 28.3, wins_list)
print(e1, e2, e3)

# MINIMISATION
# need to wrap whole thing in a function
# also, lots of minimisation methods don't allow bounding for negative values. Let's cheat!
# return a bloody huge error if things are negative
def min_func(inputs):
    variance = inputs[0]
    draw_mar = inputs[1]

    win_list = list()
    var_list.append(variance)
    draw_mar_list.append(draw_mar)

    for i in range(0, 5 * 10 ** 4):

        #print(variance, draw_mar)
        z = simulate_game(teams, 'Team_1', 'Team_2', variance, draw_mar)
        win_list.append(z)

    e1, e2, e3 = squared_error_metric(33.1, 38.5, 28.3, win_list)
    e_sum = e1 + e2 + e3
    # print(variance, draw_mar)
    # print(e1, e2, e3, e_sum)

    del win_list

    # return e1, e2, e3
    return e_sum**0.5


# team dictionary for testing
teams = {}
teams['Team_1'] = float(115.57 * (10**6))
teams['Team_2'] = float(91.71 * (10**6))

var_list = list()
draw_mar_list = list()
var_list.append(0)
draw_mar_list.append(0)

spread_var = 0.0
while spread_var <= 0.02:
    inputs = numpy.array([(0.99+spread_var), (5.0)])

    values = scipy.optimize.minimize(min_func, inputs, args=(), method='L-BFGS-B', jac=None, hess=None, hessp=None,
                            bounds=((0,None),(0,None)), constraints=(), tol=None, callback=None, options={'disp': True})
    spread_var += 0.002

    # values = scipy.optimize.root(min_func, inputs, args=(), method='lm', jac=None, tol=None, callback=None, options=None)

    print(spread_var+0.5)
    print(values)
    print('var = ', var_list[-1], 'draw_margin = ', draw_mar_list[-1])
    del var_list
    del draw_mar_list

    var_list = list()
    draw_mar_list = list()
    var_list.append(0)
    draw_mar_list.append(0)
"""

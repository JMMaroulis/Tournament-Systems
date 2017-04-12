# dictionary of teams
import xlrd
# import csv
import All_Play_All
import Single_Game
import copy
import operator
import gc
import random


# simulate random league
def random_league_run(var_pow, draw_window, n, num_teams, n_top_teams, n_bottom_teams, xlsx_location):

    #print(n)

    # open spreadsheet
    workbook = xlrd.open_workbook(xlsx_location)
    worksheet = workbook.sheet_by_index(0)

    # declare dictionaries and lists
    random_team_payroll = {}
    random_team_score_simulated = {}
    random_team_position = {}
    random_team_position_simulated = {}
    random_team_name_list = []

    # populate payroll and initial score dictionaries for twenty most prevalent teams
    for i in range(1, num_teams+1):
        random_team_payroll[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 1).value
        random_team_score_simulated[str(worksheet.cell(i, 0).value)] = 0
        random_team_name_list.append(str(worksheet.cell(i, 0).value))
        random_team_position[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 6).value

    # print(random_team_payroll)
    # print(random_team_position)
    # print(random_team_score)
    for y in range(0, n):

        gc.disable()
        # EACH TEAM PLAYS A RANDOM DIFFERENT TEAM N TIMES
        All_Play_All.all_play_random(random_team_payroll, random_team_score_simulated, var_pow, draw_window, 1)
        gc.collect()

    # take average of scores
    for w in random_team_score_simulated:
        random_team_score_simulated[w] /= float(n)

    # CALCULATE POSITION DIFFERENCE METRIC

    # calculate team positions
    placehold = copy.deepcopy(random_team_score_simulated)
    placehold.items()
    placehold = [(v, k) for k, v in placehold.iteritems()]
    placehold.sort()
    #print(placehold)
    for i in range(0, len(placehold)):
        random_team_position_simulated[placehold[len(placehold) - (i+1)][1]] = i+1

    # calculate differences
    position_metric = 0
    for team in random_team_position_simulated:
        position_metric += abs(random_team_position[team] - random_team_position_simulated[team])**1.0
        #print(team)
        #print(random_team_position[team])
        #print(random_team_position_simulated[team])
        #print(position_metric)
    #position_metric **= 2
    #print(position_metric)

    sorted_team_positions_simulated = sorted(random_team_position_simulated.items(), key=operator.itemgetter(1))
    sorted_team_score_simulated = sorted(random_team_score_simulated.items(), key=operator.itemgetter(1))
    sorted_team_position = sorted(random_team_score_simulated.items(), key=operator.itemgetter(1))

    # calculate position metric of top x teams
    x = n_top_teams
    top_teams_position_error = 0.0
    while x != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[int(len(sorted_team_position) - (x))][0]
        top_teams_position_error += abs(random_team_position[team] - random_team_position_simulated[team])**1.0
        x -= 1

    # calculate position metric of bottom x teams
    z = n_bottom_teams
    bottom_teams_position_error = 0.0
    length = len(sorted_team_position)
    while z != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[z-1][0]
        bottom_teams_position_error += abs(random_team_position[team] - random_team_position_simulated[team])**1.0
        z -= 1

    # print(sorted_team_positions_simulated)
    # print(sorted_team_score_simulated)

    for i in sorted_team_positions_simulated:
        #print(i)
        pass

    for i in sorted_team_score_simulated:
        #print(i)
        pass

    gc.collect()
    return position_metric, top_teams_position_error, bottom_teams_position_error

if __name__ == "__main__":
    print(random_league_run(0.0, 0.0, 10**0, 20, 5, 5, 'Uniform_Team.xlsx'))


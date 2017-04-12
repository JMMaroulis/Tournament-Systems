# dictionary of teams
import xlrd
# import csv
import All_Play_All
import copy
import operator
import gc
import scipy.stats


# simulate premier league
def premier_league_run(var_pow, draw_window, n, num_teams, n_top_teams, n_bottom_teams, xlsx_location):

    #print(n)

    # open spreadsheet
    workbook = xlrd.open_workbook(xlsx_location)
    worksheet = workbook.sheet_by_index(0)

    # declare dictionaries and lists
    premier_team_payroll = {}
    premier_team_score = {}
    premier_team_score_simulated = {}
    premier_team_position = {}
    premier_team_position_simulated = {}
    premier_team_name_list = []

    # populate payroll and initial score dictionaries for twenty most prevalent teams
    for i in range(1, num_teams+1):
        premier_team_payroll[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 1).value
        premier_team_score[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 3).value
        premier_team_score_simulated[str(worksheet.cell(i, 0).value)] = 0
        premier_team_name_list.append(str(worksheet.cell(i, 0).value))
        premier_team_position[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 6).value

    # print(premier_team_payroll)
    # print(premier_team_position)
    # print(premier_team_score)

    gc.disable()
    # play 2 round robin n times
    for y in range(0, int(n)):
        All_Play_All.n_round_robin(premier_team_payroll, premier_team_score_simulated, var_pow, draw_window, 2)
    gc.collect()

    # CALCULATE DRAW METRIC
    # number of games in premier league = 380
    # calculate number of draws
    points_sum = 0
    for z in premier_team_name_list:
        points_sum += premier_team_score_simulated[z]
    num_draws = (380*3*n) - points_sum
    num_draws_av = num_draws/n
    # print('Average Number of Draws =', num_draws_av)

    # AVERAGE #DRAWS IN PREMIER LEAGUE = 98.35714286
    draw_error = abs(num_draws_av - 87.3851370899997)

    # take average of scores
    for w in premier_team_score_simulated:
        premier_team_score_simulated[w] /= float(n)

    # CALCULATE SCORE DIFFERENCE METRIC
    score_diff_metric = 0
    for name in premier_team_name_list:
        score_diff_metric += abs(premier_team_score_simulated[name] - premier_team_score[name])**1.0
        #print(score_diff_metric)
    #score_diff_metric **= 2

    # print(score_diff_metric)

    # CALCULATE POSITION DIFFERENCE METRIC

    # calculate team positions
    placehold = copy.deepcopy(premier_team_score_simulated)
    placehold.items()
    placehold = [(v, k) for k, v in placehold.iteritems()]
    placehold.sort()
    #print(placehold)
    for i in range(0, len(placehold)):
        premier_team_position_simulated[placehold[len(placehold) - (i+1)][1]] = i+1

    # calculate differences
    position_metric = 0
    for team in premier_team_position_simulated:
        position_metric += abs(premier_team_position[team] - premier_team_position_simulated[team])**1.0
        #print(team)
        #print(premier_team_position[team])
        #print(premier_team_position_simulated[team])
        #print(position_metric)
    #position_metric **= 2
    #print(position_metric)

    sorted_team_positions_simulated = sorted(premier_team_position_simulated.items(), key=operator.itemgetter(1))
    sorted_team_score_simulated = sorted(premier_team_score_simulated.items(), key=operator.itemgetter(1))
    sorted_team_position = sorted(premier_team_score_simulated.items(), key=operator.itemgetter(1))

    # calculate position metric of top x teams
    x = n_top_teams
    top_teams_position_error = 0.0
    while x != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[int(len(sorted_team_position)-x)][0]
        top_teams_position_error += abs(premier_team_position[team] - premier_team_position_simulated[team])**1.0
        x -= 1

    # calculate position metric of bottom x teams
    z = n_bottom_teams
    bottom_teams_position_error = 0.0
    while z != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[z - 1][0]
        bottom_teams_position_error += abs(premier_team_position[team] - premier_team_position_simulated[team])**1.0
        z -= 1

    # print(sorted_team_positions_simulated)
    # print(sorted_team_score_simulated)

    for i in sorted_team_positions_simulated:
        # print(i)
        pass

    for i in sorted_team_score_simulated:
        # print(i)
        pass

    gc.collect()
    return score_diff_metric, draw_error, position_metric, top_teams_position_error, bottom_teams_position_error

if __name__ == "__main__":
    print(premier_league_run(1.1, 0.5, 10**0, 20, 3, 3, 'Uniform_Team.xlsx'))


# dictionary of teams
import xlrd
# import csv
import All_Play_All
import copy
import operator
import gc


def scottish_premier_league_run(var_pow, draw_window, n, num_teams, n_top_teams, n_bottom_teams, xlsx_location):

    # open spreadsheet
    workbook = xlrd.open_workbook(xlsx_location)
    worksheet = workbook.sheet_by_index(0)

    # declare dictionaries and lists
    premier_team_payroll = {}
    premier_team_score_simulated = {}
    premier_team_position = {}
    premier_team_position_simulated = {}
    premier_team_name_list = []

    # populate payroll and initial score dictionaries for teams in worksheet
    for i in range(1, num_teams+1):
        premier_team_payroll[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 1).value
        premier_team_score_simulated[str(worksheet.cell(i, 0).value)] = 0
        premier_team_name_list.append(str(worksheet.cell(i, 0).value))
        premier_team_position[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 6).value

    for y in range(0, int(n)):

        gc.disable()
        # all play all 3 times
        All_Play_All.n_round_robin(premier_team_payroll, premier_team_score_simulated, var_pow, draw_window, 3)
        gc.collect()

        # THE SPLIT
        # split teams into top half and bottom half
        premier_team_score_simulated_sorted = sorted(premier_team_score_simulated.items(), key=operator.itemgetter(1))

        # top half
        premier_team_payroll_top = {}
        premier_team_score_simulated_top = {}

        # bottom half
        premier_team_payroll_bottom = {}
        premier_team_score_simulated_bottom = {}

        # create top half of split
        # reset simulated points values
        for i in premier_team_score_simulated_sorted[int(len(premier_team_score_simulated)/2):]:
            # pulling values from prior dictionaries based on sorting of tuple list
            premier_team_payroll_top[i[0]] = premier_team_payroll[i[0]]
            premier_team_score_simulated_top[i[0]] = premier_team_score_simulated[i[0]] + 20000

        # create bottom half of split
        for i in premier_team_score_simulated_sorted[:int(len(premier_team_score_simulated)/2)]:
            # pulling values from prior dictionaries based on sorting of tuple list
            premier_team_payroll_bottom[i[0]] = premier_team_payroll[i[0]]
            premier_team_score_simulated_bottom[i[0]] = premier_team_score_simulated[i[0]]

        # top half - all play all once
        All_Play_All.n_round_robin(premier_team_payroll_top, premier_team_score_simulated_top, var_pow, draw_window, 1)
        # bottom half - all play all once
        All_Play_All.n_round_robin(premier_team_payroll_bottom, premier_team_score_simulated_bottom, var_pow, draw_window, 1)

        # re-merge score dictionaries
        premier_team_score_simulated = copy.deepcopy(premier_team_score_simulated_top)
        premier_team_score_simulated.update(premier_team_score_simulated_bottom)

    # take average of scores
    for w in premier_team_score_simulated:
        premier_team_score_simulated[w] /= float(n)

    # CALCULATE POSITION DIFFERENCE METRIC

    # calculate team positions
    placehold = copy.deepcopy(premier_team_score_simulated)
    placehold.items()
    placehold = [(v, k) for k, v in placehold.iteritems()]
    placehold.sort()
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
    sorted_team_position = sorted(premier_team_position.items(), key=operator.itemgetter(1))

    # calculate position metric of top x teams
    x = n_top_teams
    top_teams_position_error = 0.0
    while x != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[x-1][0]
        top_teams_position_error += abs(premier_team_position[team] - premier_team_position_simulated[team])**1.0
        x -= 1

    # calculate position metric of bottom x teams
    z = n_bottom_teams
    bottom_teams_position_error = 0.0
    length = len(sorted_team_position)
    while z != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[int(length - (z))][0]
        bottom_teams_position_error += (premier_team_position[team] - premier_team_position_simulated[team])**1.0
        z -= 1

    for i in sorted_team_positions_simulated:
        # print(i)
        pass

    for i in sorted_team_score_simulated:
        # print(i)
        pass

    gc.collect()

    return position_metric, top_teams_position_error, bottom_teams_position_error

if __name__ == "__main__":

    print(scottish_premier_league_run(0.0, 0.0, 10**0, 20, 3, 3, 'Uniform_Team.xlsx'))


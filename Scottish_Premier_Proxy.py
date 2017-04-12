import Premier_League
import Scottish_Premier_League
import Purely_Random_Tournament
import All_Play_All
import Single_Game
import gc
import xlrd
import copy
import operator
import random

# using one round robin, the split, and another 2 round robins in each half to make a pseudo-scottish premier league
# the idea being to match the number of games in the english premier league as closely as possible
# requires 20 teams for the maths to work


def scottish_pseudo_league_run(var_pow, draw_window, n, num_teams, n_top_teams, n_bottom_teams, xlsx_location):

    # open spreadsheet
    workbook = xlrd.open_workbook(xlsx_location)
    worksheet = workbook.sheet_by_index(0)

    # declare dictionaries and lists
    pseudo_team_payroll = {}
    pseudo_team_score_simulated = {}
    pseudo_team_position = {}
    pseudo_team_position_simulated = {}
    pseudo_team_name_list = []

    # populate payroll and initial score dictionaries for teams in worksheet
    for i in range(1, num_teams+1):
        pseudo_team_payroll[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 1).value
        pseudo_team_score_simulated[str(worksheet.cell(i, 0).value)] = 0
        pseudo_team_name_list.append(str(worksheet.cell(i, 0).value))
        pseudo_team_position[str(worksheet.cell(i, 0).value)] = worksheet.cell(i, 6).value

    for y in range(0, int(n)):

        gc.disable()
        # all play all once
        All_Play_All.n_round_robin(pseudo_team_payroll, pseudo_team_score_simulated, var_pow, draw_window, 1)
        gc.collect()

        # THE SPLIT
        # split teams into top half and bottom half
        pseudo_team_score_simulated_sorted = sorted(pseudo_team_score_simulated.items(), key=operator.itemgetter(1))

        # top half
        pseudo_team_payroll_top = {}
        pseudo_team_score_simulated_top = {}

        # bottom half
        pseudo_team_payroll_bottom = {}
        pseudo_team_score_simulated_bottom = {}

        # create top half of split
        # reset simulated points values
        for i in pseudo_team_score_simulated_sorted[int(len(pseudo_team_score_simulated_sorted)/2):]:
            # pulling values from prior dictionaries based on sorting of tuple list
            pseudo_team_payroll_top[i[0]] = pseudo_team_payroll[i[0]]
            pseudo_team_score_simulated_top[i[0]] = pseudo_team_score_simulated[i[0]] + 200000


        # create bottom half of split
        for i in pseudo_team_score_simulated_sorted[:int(len(pseudo_team_score_simulated_sorted)/2)]:
             # pulling values from prior dictionaries based on sorting of tuple list
            pseudo_team_payroll_bottom[i[0]] = pseudo_team_payroll[i[0]]
            pseudo_team_score_simulated_bottom[i[0]] = pseudo_team_score_simulated[i[0]]

        # top half - all play all twice
        All_Play_All.n_round_robin(pseudo_team_payroll_top, pseudo_team_score_simulated_top, var_pow, draw_window, 2)
        # bottom half - all play all twice
        All_Play_All.n_round_robin(pseudo_team_payroll_bottom, pseudo_team_score_simulated_bottom, var_pow, draw_window, 2)

        # re-merge score dictionaries
        pseudo_team_score_simulated = copy.deepcopy(pseudo_team_score_simulated_top)
        pseudo_team_score_simulated.update(pseudo_team_score_simulated_bottom)

        # one last random round
        for team_home in pseudo_team_payroll:
            team_subset = copy.deepcopy(pseudo_team_payroll)
            # remove home team from subset
            del team_subset[team_home]

            # play a random person in that dict, score points from results
            random_away_team = random.choice(team_subset.keys())

            result = Single_Game.simulate_game(pseudo_team_payroll, team_home, random_away_team, var_pow, draw_window)
            All_Play_All.give_points(result, pseudo_team_score_simulated, team_home, random_away_team)


    # take average of scores
    for w in pseudo_team_score_simulated:
        pseudo_team_score_simulated[w] /= float(n)

    # CALCULATE POSITION DIFFERENCE METRIC

    # calculate team positions
    placehold = copy.deepcopy(pseudo_team_score_simulated)
    placehold.items()
    placehold = [(v, k) for k, v in placehold.iteritems()]
    placehold.sort()
    for i in range(0, len(placehold)):
        pseudo_team_position_simulated[placehold[len(placehold) - (i+1)][1]] = i+1

    # calculate differences
    position_metric = 0
    for team in pseudo_team_position_simulated:
        position_metric += abs(pseudo_team_position[team] - pseudo_team_position_simulated[team])**1.0
        #print(team)
        #print(pseudo_team_position[team])
        #print(pseudo_team_position_simulated[team])
        #print(position_metric)
    #position_metric **= 2
    #print(position_metric)

    sorted_team_positions_simulated = sorted(pseudo_team_position_simulated.items(), key=operator.itemgetter(1))
    sorted_team_score_simulated = sorted(pseudo_team_score_simulated.items(), key=operator.itemgetter(1))
    sorted_team_position = sorted(pseudo_team_position.items(), key=operator.itemgetter(1))

    # calculate position metric of top x teams
    x = n_top_teams
    top_teams_position_error = 0.0
    while x != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[x-1][0]
        top_teams_position_error += abs(pseudo_team_position[team] - pseudo_team_position_simulated[team])**1.0
        x -= 1

    # calculate position metric of bottom x teams
    z = n_bottom_teams
    bottom_teams_position_error = 0.0
    length = len(sorted_team_position)
    while z != 0:
        # grab teams expected to be top, add error
        team = sorted_team_position[int(length - (z))][0]
        bottom_teams_position_error += abs(pseudo_team_position[team] - pseudo_team_position_simulated[team])**1.0
        z -= 1

    for i in sorted_team_positions_simulated:
        # print(i)
        pass

    for i in sorted_team_score_simulated:
        # print(i)
        pass

    gc.collect()

    for i in sorted_team_positions_simulated:
        # print(i)
        pass

    return position_metric, top_teams_position_error, bottom_teams_position_error

if __name__ == "__main__":

    print(scottish_pseudo_league_run(1.1, 0.5, 10**3, 20, 5, 5, 'Uniform_Team.xlsx'))


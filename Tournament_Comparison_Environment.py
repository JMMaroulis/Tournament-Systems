import Premier_League
import Scottish_Premier_League
import Scottish_Premier_Proxy
import Purely_Random_Tournament
import All_Play_All
import Single_Game
import gc
import scipy.stats

num_leagues = int(1000)
bottom_range = 5
top_range = 101
num_teams_top = 5
num_teams_bottom = num_teams_top
xlsx_file = "Uniform_Team.xlsx"


# ENGLISH PREMIER LEAGUE ERROR DERIVATION
# var, draw, leagues per run, n_top_teams, n_bottom_teams
# 0.0, 0.501333798323, 10**0, 6, 6
english_premier_position_error_list = list()
english_premier_top_position_error_list = list()
english_premier_bottom_position_error_list = list()
position_mean_error_list_external = list()
top_position_mean_error_list_external = list()
bottom_position_mean_error_list_external = list()


num_teams_list = list()
num_games_list = list()


for n_teams in range(bottom_range, top_range):

    print('running english premier league at n_teams = ', n_teams)

    english_premier_position_error = 0.0
    english_premier_top_position_error = 0.0
    english_premier_bottom_position_error = 0.0
    position_error_list_internal = list()
    top_position_error_list_internal = list()
    bottom_position_error_list_internal = list()

    gc.disable()
    for i in range(0, num_leagues):
        results = Premier_League.premier_league_run(1.15105, 0.48577, 1, n_teams, num_teams_top, num_teams_bottom, xlsx_file)
        english_premier_position_error += results[2]
        english_premier_top_position_error += results[3]
        english_premier_bottom_position_error += results[4]
        position_error_list_internal.append(results[2])
        top_position_error_list_internal.append(results[3])
        bottom_position_error_list_internal.append(results[4])
    gc.collect()

    # calculate error on mean over all reported errors from multiple leagues
    position_mean_error = scipy.stats.sem(position_error_list_internal)
    position_mean_error_top = scipy.stats.sem(top_position_error_list_internal)
    position_mean_error_bottom = scipy.stats.sem(bottom_position_error_list_internal)

    # average out over all leagues
    english_premier_position_error /= num_leagues
    english_premier_top_position_error /= num_leagues
    english_premier_bottom_position_error /= num_leagues

    # put data in lists for printing to file later
    english_premier_position_error_list.append(english_premier_position_error)
    english_premier_top_position_error_list.append(english_premier_top_position_error)
    english_premier_bottom_position_error_list.append(english_premier_bottom_position_error)
    num_teams_list.append(n_teams)
    position_mean_error_list_external.append(position_mean_error)
    top_position_mean_error_list_external.append(position_mean_error_top)
    bottom_position_mean_error_list_external.append(position_mean_error_bottom)

    del position_error_list_internal
    del top_position_error_list_internal
    del bottom_position_error_list_internal
    gc.collect()

    print('pos error:', english_premier_position_error)
    print('pos error top:', english_premier_top_position_error)
    print('pos error bottom:', english_premier_bottom_position_error)

# put in file
english_premier_txt = open('english_premier_position.txt', 'w')
for i in range(0, len(english_premier_position_error_list)):
    english_premier_txt.write('%s' % num_teams_list[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s' % english_premier_position_error_list[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s' % english_premier_top_position_error_list[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s' % english_premier_bottom_position_error_list[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s' % position_mean_error_list_external[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s' % top_position_mean_error_list_external[i])
    english_premier_txt.write(' ')
    english_premier_txt.write('%s\n' % bottom_position_mean_error_list_external[i])
english_premier_txt.close()

# SCOTTISH PREMIER LEAGUE ERROR DERIVATION
# var, draw, leagues per run, n_top_teams, n_bottom_teams
# 0.0, 0.501333798323, 10**0, 6, 6


scottish_premier_position_error_list = list()
scottish_premier_top_position_error_list = list()
scottish_premier_bottom_position_error_list = list()
position_mean_error_list_external = list()
top_position_mean_error_list_external = list()
bottom_position_mean_error_list_external = list()
num_teams_list = list()

for n_teams in range(bottom_range, top_range):
    print('running scottish premier league at n_teams = ', n_teams)

    scottish_premier_position_error = 0.0
    scottish_premier_top_position_error = 0.0
    scottish_premier_bottom_position_error = 0.0
    position_error_list_internal = list()
    top_position_error_list_internal = list()
    bottom_position_error_list_internal = list()

    for i in range(0, num_leagues):
        results = Scottish_Premier_League.scottish_premier_league_run(1.15105, 0.48577, 1, n_teams, num_teams_top, num_teams_bottom, 'Uniform_Team.xlsx')
        scottish_premier_position_error += results[0]
        scottish_premier_top_position_error += results[1]
        scottish_premier_bottom_position_error += results[2]
        position_error_list_internal.append(results[0])
        top_position_error_list_internal.append(results[1])
        bottom_position_error_list_internal.append(results[2])
        gc.collect()

    # calculate error on mean over all reported errors from multiple leagues
    position_mean_error = scipy.stats.sem(position_error_list_internal)
    position_mean_error_top = scipy.stats.sem(top_position_error_list_internal)
    position_mean_error_bottom = scipy.stats.sem(bottom_position_error_list_internal)

    scottish_premier_position_error /= num_leagues
    scottish_premier_top_position_error /= num_leagues
    scottish_premier_bottom_position_error /= num_leagues

    scottish_premier_position_error_list.append(scottish_premier_position_error)
    scottish_premier_top_position_error_list.append(scottish_premier_top_position_error)
    scottish_premier_bottom_position_error_list.append(scottish_premier_bottom_position_error)
    num_teams_list.append(n_teams)
    position_mean_error_list_external.append(position_mean_error)
    top_position_mean_error_list_external.append(position_mean_error_top)
    bottom_position_mean_error_list_external.append(position_mean_error_bottom)

    del position_error_list_internal
    del top_position_error_list_internal
    del bottom_position_error_list_internal
    gc.collect()

    print('pos error:', scottish_premier_position_error)
    print('pos error top:', scottish_premier_top_position_error)
    print('pos error bottom:', scottish_premier_bottom_position_error)

# put in file
print(scottish_premier_position_error_list)

scottish_premier_txt = open('scottish_premier_position.txt', 'w')
for i in range(0, len(scottish_premier_position_error_list)):
    scottish_premier_txt.write('%s' % num_teams_list[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s' % scottish_premier_position_error_list[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s' % scottish_premier_top_position_error_list[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s' % scottish_premier_bottom_position_error_list[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s' % position_mean_error_list_external[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s' % top_position_mean_error_list_external[i])
    scottish_premier_txt.write(' ')
    scottish_premier_txt.write('%s\n' % bottom_position_mean_error_list_external[i])
scottish_premier_txt.close()



# RANDOM LEAGUE ERROR DERIVATION
# var, draw, leagues per run, n_top_teams, n_bottom_teams
# 0.0, 0.501333798323, 10**0, 6, 6
random_position_error_list = list()
random_top_position_error_list = list()
random_bottom_position_error_list = list()
position_mean_error_list_external = list()
top_position_mean_error_list_external = list()
bottom_position_mean_error_list_external = list()
num_teams_list = list()

for n_teams in range(bottom_range, top_range):

    print('running random league at n_teams = ', n_teams)

    random_position_error = 0.0
    random_top_position_error = 0.0
    random_bottom_position_error = 0.0
    position_error_list_internal = list()
    top_position_error_list_internal = list()
    bottom_position_error_list_internal = list()

    gc.disable()
    for i in range(0, num_leagues):
        results = Purely_Random_Tournament.random_league_run(1.15105, 0.48577, 1, n_teams, num_teams_top, num_teams_bottom, xlsx_file)
        random_position_error += results[0]
        random_top_position_error += results[1]
        random_bottom_position_error += results[2]
        position_error_list_internal.append(results[0])
        top_position_error_list_internal.append(results[1])
        bottom_position_error_list_internal.append(results[2])
    gc.collect()

    # calculate error on mean over all reported errors from multiple leagues
    position_mean_error = scipy.stats.sem(position_error_list_internal)
    position_mean_error_top = scipy.stats.sem(top_position_error_list_internal)
    position_mean_error_bottom = scipy.stats.sem(bottom_position_error_list_internal)


    random_position_error /= num_leagues
    random_top_position_error /= num_leagues
    random_bottom_position_error /= num_leagues

    random_position_error_list.append(random_position_error)
    random_top_position_error_list.append(random_top_position_error)
    random_bottom_position_error_list.append(random_bottom_position_error)
    num_teams_list.append(n_teams)
    position_mean_error_list_external.append(position_mean_error)
    top_position_mean_error_list_external.append(position_mean_error_top)
    bottom_position_mean_error_list_external.append(position_mean_error_bottom)

    del position_error_list_internal
    del top_position_error_list_internal
    del bottom_position_error_list_internal
    gc.collect()

    print('pos error:', random_position_error)
    print('pos error top:', random_top_position_error)
    print('pos error bottom:', random_bottom_position_error)

# put in file
print(random_position_error_list)

random_txt = open('random_position.txt', 'w')
for i in range(0, len(random_position_error_list)):
    random_txt.write('%s' % num_teams_list[i])
    random_txt.write(' ')
    random_txt.write('%s' % random_position_error_list[i])
    random_txt.write(' ')
    random_txt.write('%s' % random_top_position_error_list[i])
    random_txt.write(' ')
    random_txt.write('%s' % random_bottom_position_error_list[i])
    random_txt.write(' ')
    random_txt.write('%s' % position_mean_error_list_external[i])
    random_txt.write(' ')
    random_txt.write('%s' % top_position_mean_error_list_external[i])
    random_txt.write(' ')
    random_txt.write('%s\n' % bottom_position_mean_error_list_external[i])
random_txt.close()
random_txt.close()



# SCOTTISH PSEUDO-PREMIER LEAGUE ERROR DERIVATION
# var, draw, leagues per run, n_top_teams, n_bottom_teams
# 0.0, 0.501333798323, 10**0, 6, 6


scottish_pseudo_position_error_list = list()
scottish_pseudo_top_position_error_list = list()
scottish_pseudo_bottom_position_error_list = list()
position_error_list_external = list()
top_position_error_list_external = list()
bottom_position_error_list_external = list()

num_teams_list = list()

for n_teams in range(bottom_range, top_range):
    print('running scottish pseudo league at n_teams = ', n_teams)

    scottish_pseudo_position_error = 0.0
    scottish_pseudo_top_position_error = 0.0
    scottish_pseudo_bottom_position_error = 0.0
    position_error_list_internal = list()
    top_position_error_list_internal = list()
    bottom_position_error_list_internal = list()

    for i in range(0, num_leagues):
        results = Scottish_Premier_Proxy.scottish_pseudo_league_run(1.15105, 0.48577, 1, n_teams, num_teams_top, num_teams_bottom, xlsx_file)
        scottish_pseudo_position_error += results[0]
        scottish_pseudo_top_position_error += results[1]
        scottish_pseudo_bottom_position_error += results[2]
        position_error_list_internal.append(results[0])
        top_position_error_list_internal.append(results[1])
        bottom_position_error_list_internal.append(results[2])
    gc.collect()

    # calculate error on mean over all reported errors from multiple leagues
    position_mean_error = scipy.stats.sem(position_error_list_internal)
    position_mean_error_top = scipy.stats.sem(top_position_error_list_internal)
    position_mean_error_bottom = scipy.stats.sem(bottom_position_error_list_internal)

    scottish_pseudo_position_error /= num_leagues
    scottish_pseudo_top_position_error /= num_leagues
    scottish_pseudo_bottom_position_error /= num_leagues

    scottish_pseudo_position_error_list.append(scottish_pseudo_position_error)
    scottish_pseudo_top_position_error_list.append(scottish_pseudo_top_position_error)
    scottish_pseudo_bottom_position_error_list.append(scottish_pseudo_bottom_position_error)
    num_teams_list.append(n_teams)
    position_mean_error_list_external.append(position_mean_error)
    top_position_mean_error_list_external.append(position_mean_error_top)
    bottom_position_mean_error_list_external.append(position_mean_error_bottom)

    del position_error_list_internal
    del top_position_error_list_internal
    del bottom_position_error_list_internal
    gc.collect()

    print('pos error:', scottish_pseudo_position_error)
    print('pos error top:', scottish_pseudo_top_position_error)
    print('pos error bottom:', scottish_pseudo_bottom_position_error)

# put in file
print(scottish_pseudo_position_error_list)

scottish_pseudo_txt = open('scottish_pseudo_position.txt', 'w')
for i in range(0, len(scottish_pseudo_position_error_list)):
    scottish_pseudo_txt.write('%s' % num_teams_list[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s' % scottish_pseudo_position_error_list[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s' % scottish_pseudo_top_position_error_list[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s' % scottish_pseudo_bottom_position_error_list[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s' % position_mean_error_list_external[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s' % top_position_mean_error_list_external[i])
    scottish_pseudo_txt.write(' ')
    scottish_pseudo_txt.write('%s\n' % bottom_position_mean_error_list_external[i])
scottish_pseudo_txt.close()



"""
# ADDENDUM
# Triangular number calculator might come in handy later

# Calculate number of games played
# twice the nth triangular number for n teams
n_count = n_teams
n_triangle = 0.0
while n_count != 0:
    n_triangle += n_count
    n_count -= 1
print(n_triangle)

random_position_error /= (num_random_rounds * n_triangle)
random_top_position_error /= (num_random_rounds * n_triangle)
random_bottom_position_error /= (num_random_rounds * n_triangle)
"""



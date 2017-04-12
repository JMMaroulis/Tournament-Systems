import Single_Game
import All_Play_All
import Premier_League
import numpy
import scipy
import gc
from operator import itemgetter
import sys


gc.disable()
# MINIMISATION
# need to wrap whole thing in a function
# also, lots of minimisation methods don't allow bounding for negative values. Let's cheat!
# return a bloody huge error if things are negative?

results_points_metric_super = []
results_points_metric_sub = []
results_draw_metric_sub = []
results_draw_metric_super = []
results_position_metric_sub = []
results_position_metric_super = []
results_sub = []
results_super = []


def min_func(inputs):
    variance = inputs[0]
    draw_mar = inputs[1]
    n = inputs[2]

    score_metric, draw_metric, position_metric = Premier_League.premier_league_run(variance, draw_mar, n)

    results_points_metric_sub.append((score_metric, draw_metric, position_metric, variance, draw_mar))
    results_draw_metric_sub.append((draw_metric, score_metric, position_metric, variance, draw_mar))
    results_position_metric_sub.append((position_metric, draw_metric, score_metric, variance, draw_mar))
    #results_sub.append((score_metric, draw_metric, position_metric, variance, draw_mar))

    # print(variance, draw_mar, z)
    # return score_metric, draw_metric, position_metric
    return score_metric, draw_metric, position_metric

# defined variables for run

"""
var_start_value = 10.0 ** 6
var_end_value = 10.0 ** 7
spread_var_increment = 10.0 ** 6
draw_start_value = 0.01
draw_end_value = 0.05
spread_draw_increment = 0.01
"""


var_start_value = 0.5
var_end_value = 1.5
spread_var_increment = 0.05
draw_start_value = 0.5
draw_end_value = 1.5
spread_draw_increment = 0.05


spread_var = 0.0
spread_draw = 0.0
#for j in range(0, int(abs(draw_start_value - draw_end_value / spread_draw_increment))):
while (spread_draw + draw_start_value) <= draw_end_value:
    while (spread_var + var_start_value) <= var_end_value:

        inputs = numpy.array([(var_start_value + spread_var), (draw_start_value + spread_draw), int(10 ** 3)])

        values = scipy.optimize.minimize(min_func, inputs, args=(), method='COBYLA', jac=None, hess=None, hessp=None,
                                bounds=((0.0001, None), (0.0001, None), (10**3, 10**3)), constraints=(), tol=None, callback=None, options={'disp': False})

        # take most successful sub-iteration, put in list
        results_points_metric_sub.sort()
        results_draw_metric_sub.sort()
        results_position_metric_sub.sort()

        print(results_points_metric_sub[0])

        results_points_metric_super.append(results_points_metric_sub[0])
        results_draw_metric_super.append(results_draw_metric_sub[0])
        results_position_metric_super.append(results_position_metric_sub[0])

        gc.enable()
        del results_points_metric_sub[:]
        del results_draw_metric_sub[:]
        del results_position_metric_sub[:]
        del results_sub[:]
        gc.collect()
        gc.disable()

        # bounds=((0, None), (0, None), (0, None))

        # print(values)
        print('inputs:', inputs)

        spread_var += spread_var_increment

        # values = scipy.optimize.root(min_func, inputs, args=(), method='lm', jac=None, tol=None, callback=None, options=None)
    print("iterate2!")

    spread_draw += spread_draw_increment
    spread_var = 0.0

results_points_metric_super.sort()
results_draw_metric_super.sort()
results_position_metric_super.sort()
print(results_points_metric_super)
print(results_draw_metric_super)
print(results_position_metric_super)

# print results to files for heatmapping
min_results_score = open("min_results_score.txt", "w")
min_results_draw = open("min_results_draws.txt", "w")
min_results_position = open("min_results_position.txt", "w")

# file headers
# (yes, I know it's inefficient, no I don't care right now)
min_results_score.write('score_metric')
min_results_score.write(' ')
min_results_score.write('draw_metric')
min_results_score.write(' ')
min_results_score.write('position_metric')
min_results_score.write(' ')
min_results_score.write('var_pow')
min_results_score.write(' ')
min_results_score.write('draw_pow \n')

min_results_draw.write('score_metric')
min_results_draw.write(' ')
min_results_draw.write('draw_metric')
min_results_draw.write(' ')
min_results_draw.write('position_metric')
min_results_draw.write(' ')
min_results_draw.write('var_pow')
min_results_draw.write(' ')
min_results_draw.write('draw_pow \n')

min_results_position.write('score_metric')
min_results_position.write(' ')
min_results_position.write('draw_metric')
min_results_position.write(' ')
min_results_position.write('position_metric')
min_results_position.write(' ')
min_results_position.write('var_pow')
min_results_position.write(' ')
min_results_position.write('draw_pow \n')

for i in range(0, len(results_points_metric_super)):

    a = results_points_metric_super[i][0]
    b = results_points_metric_super[i][1]
    c = results_points_metric_super[i][2]
    d = results_points_metric_super[i][3]
    e = results_points_metric_super[i][4]

    min_results_score.write('%s' % a)
    min_results_score.write(' ')
    min_results_score.write('%s' % b)
    min_results_score.write(' ')
    min_results_score.write('%s' % c)
    min_results_score.write(' ')
    min_results_score.write('%s' % d)
    min_results_score.write(' ')
    min_results_score.write('%s \n' % e)

    a = results_draw_metric_super[i][1]
    b = results_draw_metric_super[i][0]
    c = results_draw_metric_super[i][2]
    d = results_draw_metric_super[i][3]
    e = results_draw_metric_super[i][4]

    min_results_draw.write('%s' % a)
    min_results_draw.write(' ')
    min_results_draw.write('%s' % b)
    min_results_draw.write(' ')
    min_results_draw.write('%s' % c)
    min_results_draw.write(' ')
    min_results_draw.write('%s' % d)
    min_results_draw.write(' ')
    min_results_draw.write('%s \n' % e)

    a = results_position_metric_super[i][2]
    b = results_position_metric_super[i][1]
    c = results_position_metric_super[i][0]
    d = results_position_metric_super[i][3]
    e = results_position_metric_super[i][4]

    min_results_position.write('%s' % a)
    min_results_position.write(' ')
    min_results_position.write('%s' % b)
    min_results_position.write(' ')
    min_results_position.write('%s' % c)
    min_results_position.write(' ')
    min_results_position.write('%s' % d)
    min_results_position.write(' ')
    min_results_position.write('%s \n' % e)

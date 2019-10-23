# File made just for additional agents

import numpy as np
import random as rand
import dinner_party as dp

# Referance:
# Index Swap: https://stackoverflow.com/questions/22847410/swap-two-values-in-a-numpy-array


def swap(cord1, cord2, s_table):
    ''' Given a semi optimized table, perform a switch based on given coordinates.
        If the score of the switch is suboptimal, switch it back.
    '''
    r1 = cord1[0][0]    # Get row index of cord1
    c1 = cord1[1][0]    # Get col index of cord1

    r2 = cord2[0][0]    # Get row index of cord2
    c2 = cord2[1][0]    # Get col index of cord2

    # Do fast elements swap
    s_table[r1][c1], s_table[r2][c2] = s_table[r2][c2], s_table[r1][c1]
    #print(s_table)


def local_search(s_table, pref_summed, num_p):
    '''
    '''
    sub_highest = dp.score_fast(s_table, pref_summed, num_p)   # Faster table scoring
    sub_fin_table = s_table
    #print("Sub High Score: {}\n{}\n".format(sub_highest, sub_fin_table))

    for i in range(num_p):
        # Get person's coord's
        cord_i = np.where(s_table == i)
        #print(cord_i)
        #print(cord_i[0][0])
        for j in range(num_p):
            if i == j:
                pass
            else:
                #print("i:", i, "\tj:", j)
                cord_j = np.where(s_table == j)
                swap(cord_i, cord_j, s_table)
                temp_score = dp.score_fast(s_table, pref_summed, num_p)

                if temp_score > sub_highest:
                    #print("Sub: {}\tTemp: {}".format(sub_highest, temp_score))
                    sub_highest = temp_score
                    sub_fin_table = s_table
                    # Either break or look for optimal - break first
                    break
                else:
                    # Swap it back - didn't improve score
                    #print("SWAP BACK")
                    swap(cord_j, cord_i, s_table)

    return sub_highest, sub_fin_table   # Give back the best from sub optimizations

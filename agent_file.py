# Local Search Agent file
# Name: Jordan Le
# Date: 10-23-19

import numpy as np
import random as rand
import dinner_party as dp

# Referance:
# Index Swap: https://stackoverflow.com/questions/22847410/swap-two-values-in-a-numpy-array

def swap(cord1, cord2, s_table):
    ''' Given two coordinates for elements in the 2d table and a semi optimized table,
        perform a switch based on the given coordinates.
    '''
    r1 = cord1[0][0]    # Get row index of cord1
    c1 = cord1[1][0]    # Get col index of cord1

    r2 = cord2[0][0]    # Get row index of cord2
    c2 = cord2[1][0]    # Get col index of cord2

    # Do fast elements swap
    s_table[r1][c1], s_table[r2][c2] = s_table[r2][c2], s_table[r1][c1]


def local_search(s_table, pref_summed, num_p):
    ''' Given the seated table, the transposed summed preferance matrix, and the number of people,
        calculate the optimized seated table. Then go through each person and switch them with
        another person to see if they have improved score. If they don't, swap them back. Next,
        move on to the next person and repeat the process for each set of people. Finally,
        give back the most optimal solution for the given table.
    '''
    sub_highest = dp.score_fast(s_table, pref_summed, num_p)    # Faster table scoring
    sub_fin_table = s_table                                     # Set the sub final table

    for i in range(num_p):
        cord_i = np.where(s_table == i) # Get person i's coordinates

        for j in range(num_p):          # Loop through all other people
            if i == j:                  # Don't swap the element with itself
                pass                    # Nothing to do this time
            else:
                cord_j = np.where(s_table == j)                             # Give me the coordinates of j
                swap(cord_i, cord_j, s_table)                               # Swap where i and j are
                temp_score = dp.score_fast(s_table, pref_summed, num_p)     # Calculate score fast

                if temp_score > sub_highest:        # If higher score, do updates
                    sub_highest = temp_score        # Update the sub highest score
                    sub_fin_table = s_table         # Update sub final table
                    break                           # Either break or look for optimal...
                else:           
                    swap(cord_j, cord_i, s_table)   # Swap it back, no improvement

    return sub_highest, sub_fin_table   # Give back the best from sub optimizations

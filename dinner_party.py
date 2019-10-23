# Artificial Intelligence: Dinner Party
''' Given a set of n people (n is even), they will be sat on
        two sides of a long table.

            o       o       o            o
     +-------------     ----+
     |                       ...        | 
     +-------------     ----+ 
            o       o       o            o

        Half are "hosts" half are "guests".
'''
# Name: Jordan Le
# Date: 10-5-19
# Description: Project working with state spaces. Attempting to reach maximum table score.
# Note: Final output data for each instance will be in the inst_out directory.
#       All additional output is not particularly for grading.

# Run with "python3 dinner_party.py -<agent> -<inst#>"
#   Available Agents: -rand   -greedy -final
#   Available insts:  -inst1  -inst2  -inst3

# Installs "pip3 install <package>"

# Resources:
#   - https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
#   - https://docs.scipy.org/doc/numpy/reference/generated/numpy.isin.html
#   - https://stackoverflow.com/questions/25823608/find-matching-rows-in-2-dimensional-numpy-array

import numpy as np
import random as rand
import time
import agent_file as af
import sys


# Read the text file data into 2d array. Give back 2d array and num.
def read_data(data_file="data_insts/hw1-inst1.txt"):
    ''' Read the text file data into a 2d numpy array.
        Give back 2d array and the number of people.
        ndarray data
        int num_p
    '''
    # Numpy read in my data - separate by space, skip row 1, all ints.  
    data = np.loadtxt(data_file, delimiter=" ", skiprows=1, dtype=int)
    num_p = len(data)
    print(data)
    
    return data, num_p


# Display the scoring in the correct format, then prepare to write out data
def display_scores(score, table, num_p, out_file="soln_insts/hw1-soln1.txt"):
    ''' Display the score of the final table found in the 60 seconds
        to both standard output and input specified text file.
        The text file will contain the correct format for grading.
        Note: Everyone will start at 1.
    ''' 
    fout = open(out_file, "w")                  # Output file
    line = "Table Score: {}".format(score)      # Standard line to write to file
    print(line)                                 # Display line
    fout.write(line + "\n")                     # Write to the file

    count = 1       # Initialize a count at one
    
    # Loop through the table and display as required
    for i in range(2):
        for j in range (int(num_p/2)):
            # Display current index, person + 1 because I like my zero indeces
            line = "p{} s{}".format(int(table[i][j]) + 1, count)    # Person num & Seat num
            print(line)                                             # Display line
            fout.write(line + "\n")                                 # Write to the file
            count += 1                                              # Increment count
    
    fout.close()    # Close the file
    print(table)    # Display the table for me, not grading



# Run the stuff
def main(cmd_args):
    ''' Main function which takes in command line argments to determine
        which agent to use and what hw instance to run on.
        Note: Using a transposed and element wise summed preferance
        matrix to optimize calculations later on. All the 
        h(p1, p2) + h(p2, p1) is already handled with the new matrix.
    '''

    if "-h" in cmd_args:
        print("HELP")

    # Temporary fixed argument parsing - inst is 2nd argument
    if len(cmd_args) > 2:
        inst = cmd_args[2]
        my_file = "data_insts/hw1{}.txt".format(inst)
        print(my_file)
        soln_file = "soln_insts/hw1-soln{}.txt".format(inst[5])
        print(soln_file)
        pref, num_p = read_data(my_file)                        # Create Pref table and num people specific
    else:
        pref, num_p = read_data()                               # Create Pref table and num people default
        soln_file = "soln_insts/hw1-soln1.txt".format(inst[5])  # Set default

    # Transpose matrix for simplified calculation
    tran_pref = np.transpose(pref)                      # Transpose the matrix
    pref_summed = np.add(pref, tran_pref)               # Element wise sum to save calculation later

    # Initialize variables and time
    high_score = 0                                      # Initialize my score. It better be better than 0
    fin_table_seats = np.zeros((2, int(num_p/2)))       # Initialize empty table
    states = []                                         # Initialize states - may remove
    time_left = 5                                      # Set time to 60 seconds
    start_time = time.time()                            # Start the time

    while time.time() < start_time + time_left:         # Loop while in 60 seconds
        table_seats = np.zeros((2, int(num_p/2)))       # Table
    
        if "-rand" in cmd_args: 
            s_table = rand_agent(num_p, table_seats)            # Random seated table

        elif "-greed" in cmd_args:
            s_table = agent_3(num_p, table_seats, pref_summed)  # Greedy seated table
        
        # Get the best from the optimized random placement
        sub_high, sub_fin_tab = af.local_search(s_table, pref_summed, num_p)
        if sub_high > high_score:
            high_score = sub_high
            fin_table_seats = sub_fin_tab
            print("Current Highest Table Score: ", high_score)  # Display current highest
            print(fin_table_seats)
    
    display_scores(high_score, fin_table_seats, num_p, soln_file)   # Output of final seated table score and text file


# Randomly place people at the table for the standard.
def rand_agent(num_p, table):
    ''' Random agent randomly seats people at the table and
        returns the seated table for scoring. It takes the number of people
        and an empty table.
    '''
    unseated = list(range(num_p))   # Create list from 0 - num_p

    # Loop through the table
    for i in range(2):
        for j in range (int(num_p/2)):
            # Agent select random index from unseated list
            table[i][j] = unseated[rand.randint(0, len(unseated) - 1)]

            # Remove the specified value from unseated list
            unseated.remove(table[i][j])    # Remove element by value

    return table    # Give back the table
    

# Agent Algorithm 3
def agent_3(num_p, table, pref):
    ''' Agent that takes the greedy approach and attempts to optimize early
        in the seating arrangement. It does this with a depth first local search 
        containing a greedy heuristic. This method includes random restarts 
        and noise moves in cases of the top 40% optimal moves. 
    '''
    unseated = list(range(num_p))   # Create list from 0 - num_p
    cut_off = int(num_p/2-1)

    # Place first person
    table[0][0] = unseated[rand.randint(0, len(unseated) - 1)]
    unseated.remove(table[0][0])    # remove element by value

    # Loop through the top row
    for j in range (int(num_p/2)-1):
        # Place person below and to the right
        if j == 0:  # place at bottom once
            table[1][j]= place_bot_and_side(pref, int(table[0][j]), unseated, num_p, True)          # below
            unseated.remove(table[1][j])    # remove bottom element by value
    
        if j != cut_off:
            table[0][j+1]= place_bot_and_side(pref, int(table[0][j]), unseated, num_p, False)       # right
            unseated.remove(table[0][j+1])  # remove right side element by value

        table[1][j+1] = place_corner(pref, int(table[0][j+1]), int(table[1][j]), unseated, num_p)
        unseated.remove(table[1][j+1])      # remove right side element by value

    return table    # Give back the table


def place_bot_and_side(pref, cur_per, unseated, num_p, opp):
    ''' Given the transposed summed preferance matrix, the current person,
        the unseated table, number of people, and boolean value of opposite,
        get the top 40% of optimal choices to place next to that person.
        If the optimal choices are not also in the unseated list, then 
        select the most optimal choice from everyone in the unseated.
    '''
    percent = int(num_p * .4)   # Top 40% of people 

    # The current person's favorite 4 people.
    cur_fav = np.argpartition(pref[cur_per], -percent)[-percent:]   # Their top 4 most liked people

    # Get the overlap between favorites and those unseated
    mask = np.isin(cur_fav, unseated)
    cur_fav_remaining = cur_fav[mask]   
    cur_pref_val = pref[cur_per][cur_fav_remaining]     # Their corresponding pref values

    # Are there any people who are optimal and remaining in the unseated list
    if len(cur_fav_remaining) == 0:                     # Empty list, then we go through everyone
        cur_pref_val = pref[cur_per][unseated]          # Get pref of all people to the person
        
        # Update scoring with roles
        for i in range(len(unseated)):
            cur_pref_val[i] += score_roles(cur_per, unseated[i], num_p, opp)
        
        # Best Choice
        bc_index = np.argmax(cur_pref_val)
        best_choice = unseated[bc_index]
        return best_choice

    else:   # Loop through cur's fav people and select random from remaining optimal
        
        # Update scoring with roles
        for i in range(len(cur_fav_remaining)):
            cur_pref_val[i] += score_roles(cur_per, cur_fav_remaining[i], num_p, opp)
    
        # Best Choice - select random from top remaining
        ''' # Gives me a fixed score of 85
        bc_index = np.argmax(cur_pref_val)
        best_choice = cur_fav_remaining[bc_index]
        #'''
        best_choice = cur_fav_remaining[rand.randint(0, len(cur_fav_remaining) - 1)]
        return best_choice


def place_corner(pref, cur1, cur2, unseated, num_p):
    ''' Given the summed transposed preferance matrix, the person to the top right (cur1),
        the person below (cur2), a list of the unseated people, and the total number of people,
        identify the top 40 percent of cur1 and cur2. See if they have any overlap and if 
        those people are also in the unseated list of people. If they are, randomly select
        one of the remaining optimal solutions. Otherwise, if there is no overlap, then
        look through the whole list of unseated people looking for an optimal person to place
        between cur1 and cur2.
    '''
    percent = int(num_p * .4)   # Top 40% of people

    # The current person's favorite 4 people.
    cur1_fav = np.argpartition(pref[cur1], -percent)[-percent:]     # Cur1's top 4 most liked people
    cur1_pref_val = pref[cur1][cur1_fav]                            # Cur1's corresponding pref values
    cur2_fav = np.argpartition(pref[cur2], -percent)[-percent:]     # Cur2's top 4 most liked people
    cur2_pref_val = pref[cur2][cur2_fav]                            # Cur2's corresponding pref values

    # Check if the two have any overlap
    mask = np.isin(cur1_fav, cur2_fav)                  # Do cur1 and cur2 have mutual friends
    cur_mutual_fav = cur1_fav[mask]                     # Load mutual friends
    
    # Check if the overlap from cur1 and cur2 are in the unseated list
    mask2 = np.isin(cur_mutual_fav, unseated)           # Compare cur1 & cur2 mutual friends with unseated
    cur_mutual_fav_remaining = cur_mutual_fav[mask2]    # Load remaining mutual friends

    # Check for any remaining mutual friends
    if len(cur_mutual_fav_remaining) == 0:              # If no mutual friends remaining
        pref_totals = np.zeros(len(unseated))           # Preferance totals of each

        # Look through all unseated calculate score with roles
        for i in range(len(unseated)):
            cur1_fav = pref[cur1][i] + score_roles(cur1, i, num_p, True)    # opp
            cur2_fav = pref[cur2][i] + score_roles(cur2, i, num_p, False)   # adj
            pref_totals[i] = cur1_fav + cur2_fav                            # Update pref value
        
        bc_index = np.argmax(pref_totals)   # Get index of largest pref value
        best_choice = unseated[bc_index]    # Get the best choice from the unseated

    else:
        pref_totals = np.zeros(len(cur_mutual_fav_remaining))   # Pref total of remaining

        # Look through remaining optimals
        for i in range(len(cur_mutual_fav_remaining)):
            cur1_fav = pref[cur1][i] + score_roles(cur1, i, num_p, True)    # opp
            cur2_fav = pref[cur2][i] + score_roles(cur2, i, num_p, False)   # adj
            pref_totals[i] = cur1_fav + cur2_fav                            # Update pref value

        #bc_index = np.argmax(pref_totals)                  # Get best
        #best_choice = cur_mutual_fav_remaining[bc_index]
        best_choice = cur_mutual_fav_remaining[rand.randint(0, len(cur_mutual_fav_remaining) - 1)]

    return best_choice



# Return the role of the person - host or guest?
def role(person, num):
    ''' Given a person and the number of people, identify their role.
        Then return True if they're a host and False if they're a guest.
    '''
    if person < int(num/2):     # Host if in the first half
        return True
    else:                       # Not host ie a Guest
        return False


# Return scores for roles
def score_roles(p1, p2, num, opp):
    ''' Given two people, the number of people, and a boolean opp variable.
        Determine the score to give based on role. Return 0 if the roles 
        are the same. If the roles are different, then return 1 if they
        are adjacent to one another and 2 if they're opposite of each other.
    '''
    if role(p1, num) == role(p2, num):  # If they're the same roles
        return 0                        
    else:               # If they're different roles
        if opp:         # If opposite of each other
            return 2
        else:           # They're next to each other
            return 1


# How much 1st person likes 2nd person - May be negative.
def preferance(p1, p2, pref):
    ''' Given two people and the preferance matrix, determine how much the
        1st person likes the 2nd person. However, if given the transposed
        matrix, return the sum of how much both people like each other.
    '''
    return pref[int(p1)][int(p2)]   # Return how much person 1 likes person 2


# Determine Scoring
def score_fast(s_tab, tran_pref_sum, num_p):
    ''' More efficient scoring method, given a seated table,
        the transposed/summed preferance matrix, and the number of people,
        loop through both rows and get the roles and preferances of each pair.
        Return the final score of the table.
        - 1 point for every adjacent pair (seated next to 
            each other) of people with one a host and the 
            other a guest.
        - 2 points for every opposite pair (seated across
            from each other) of people with one a host and
            the other a guest.
        - h(p1, p2) + h(p2, p1) points for every adjacent 
            or opposite pair of people p1, p2.
    '''
    score = 0
    r_score = 0
    
    for i in range(int(num_p/2)):
        score += tran_pref_sum[int(s_tab[0][i])][int(s_tab[1][i])]                  # Score for sitting accross
        r_score += score_roles(s_tab[0][i], s_tab[1][i], num_p, True)               # opps - role once

        if i < int(num_p/2 - 1):                                                    # Not on the last index
            score += tran_pref_sum[int(s_tab[0][i])][int(s_tab[0][i+1])]            # Score for top adjacent
            score += tran_pref_sum[int(s_tab[1][i])][int(s_tab[1][i+1])]            # Score for bot adjacent

            r_score += score_roles(s_tab[0][i], s_tab[0][i+1], num_p, False)        # Role adjs top
            r_score += score_roles(s_tab[1][i], s_tab[1][i+1], num_p, False)        # Role adjs bot

    return score + r_score


# Call Main
if __name__== "__main__" :
    main(sys.argv)


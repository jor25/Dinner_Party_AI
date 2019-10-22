# Artificial Intelligence: Dinner Party
''' Given a set of n people (n is even), they will be sat on
    two sides of a long table.

      o   o   o      o
   +-------------   ----+
   |             ...    | 
   +-------------   ----+ 
      o   o   o      o

    Half are "hosts" half are "guests".
'''
# Name: Jordan Le
# Date: 10-5-19
# Description: Project working with state spaces. Attempting to reach maximum table score.
# Run with "python3 dinner_party.py -<agent> -<inst#>"
# Available Agents:	-rand	-greedy	-final
# Available insts:	-inst1	-inst2	-inst3
# Installs "pip3 install <package>"
# Resources:
# 	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
#	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.isin.html

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
	#print(num_p)
	
	return data, num_p


# Display the scoring in the correct format, then prepare to write out data
def display_scores(score, table, num_p, out_file="output_testfile.txt"):
	''' Display the score of the final table found in the 60 seconds
		to both standard output and input specified text file.
		The text file will contain the correct format for grading.
		Note: Everyone will start at 1.
	'''	
	fout = open(out_file, "w")				# Output file
	line = "Table Score: {}".format(score)	# Standard line to write to file
	print(line)								# Display line
	fout.write(line + "\n")					# Write to the file

	count = 1	# Initialize a count at one
	
	# Loop through the table
	for i in range(2):
		for j in range (int(num_p/2)):
			# Display current index
			line = "p{} s{}".format(int(table[i][j]), count)	# Person num & Seat num
			print(line)											# Display line
			fout.write(line + "\n")								# Write to the file
			count += 1											# Increment count
	
	fout.close()		# Close the file
	print(table)



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

	# Some argument parsing - inst should be 2nd argument
	if len(cmd_args) > 2:
		inst = cmd_args[2]
		my_file = "data_insts/hw1{}.txt".format(inst)
		print(my_file)
		pref, num_p = read_data(my_file) 	# Create Pref table and num people
	else:
		pref, num_p = read_data() 	# Create Pref table and num people

	# Transpose matrix for simplified calculation
	tran_pref = np.transpose(pref)					# Transpose the matrix
	pref_summed = np.add(pref, tran_pref)			# Element wise sum to save calculation later
	pref_modd = pref_summed.copy()
	#print("transposed pref matrix:\n{}".format(tran_pref))
	#print(pref_summed)										# Testing elementwise summation

	# My score better be better than 0
	high_score = 0

	# Initialize empty table
	fin_table_seats = np.zeros((2, int(num_p/2)))


	time_left = 60				# 60 seconds
	start_time = time.time()	# Start time




	#testing
	'''
	table_seats = np.zeros((2, int(num_p/2)))		# Table
	af.agent_opt_3(num_p, table_seats, pref_modd)
	print(table_seats)
	print (pref_summed, '\n', pref_modd)
	#for i in range(10):
	#	af.get_top_3(i, pref_summed)
	'''





	# Initialize random table
	'''
	table_seats = np.zeros((2, int(num_p/2)))		# Table
	s_table = rand_agent(num_p, table_seats)		# Random seated table
	'''

	while time.time() < start_time + time_left:			# Loop while in 60 seconds
		table_seats = np.zeros((2, int(num_p/2)))		# Table
	
		#'''
		if "-rand" in cmd_args:	
			s_table = rand_agent(num_p, table_seats)		# Random seated table

		elif "-greed" in cmd_args:
			s_table = agent_3(num_p, table_seats, pref)		# Greedy seated table
		#table_score = scoring(s_table, pref, num_p)		# Score of seated table
		#'''
		
		# Faster table scoring
		table_score = score_fast(s_table, pref_summed, num_p)
		#print("Table score 1: {}\tTable score 2: {}".format(table_score, table_score2))

		#s_table, table_score = af.agent_inc_shuf(s_table, fin_table_seats, high_score, pref, num_p)
		
		if table_score > high_score:
			high_score = table_score	# update highest values
			fin_table_seats = s_table
			print("Current Highest Table Score: ", high_score)
	display_scores(high_score, fin_table_seats, num_p)		# Output of seated table score
	#display_scores(high_score, s_table, num_p)		# Output of seated table score


# Randomly place people at the table for the standard.
def rand_agent(num_p, table):
	''' Random agent randomly seats people at the table and
		returns the seated table for scoring. It takes the number of people
		and an empty table.
	'''
	unseated = list(range(num_p))	# Create list from 0 - num_p
	#print(unseated)

	# Loop through the table
	for i in range(2):
		for j in range (int(num_p/2)):
			# Agent select random index from unseated list
			table[i][j] = unseated[rand.randint(0, len(unseated) - 1)]

			# Remove the specified value from unseated list
			unseated.remove(table[i][j]) # remove element by value
			#print(unseated)
			#print(table)

	#print(table) # Display seating chart

	# Give back the table
	return table	
	


# Agent Algorithm 3
def agent_3(num_p, table, pref):
	unseated = list(range(num_p))	# Create list from 0 - num_p
	#print(unseated)
	
	# Select guest or host first
	goh = rand.randint(0, 1)	# 0 is guest, 1 is host
	cut_off = int(num_p/2)

	# Place first person
	table[0][0] = unseated[rand.randint(0, len(unseated) - 1)]
	unseated.remove(table[0][0]) # remove element by value
	#print(table[0][0])	


	# Loop through the top row
	for j in range (int(num_p/2)-1):
		# Place person below and to the right
		if j == 0:	# place at bottom once
			table[1][j]= place_bot_and_side(pref, int(table[0][j]), unseated, cut_off, goh)	# below
			unseated.remove(table[1][j]) # remove bottom element by value
	
		if j != cut_off:
			table[0][j+1]= place_bot_and_side(pref, int(table[0][j]), unseated, cut_off, goh)	# right
			# Remove the specified value from unseated list
			unseated.remove(table[0][j+1]) # remove right side element by value

		#print(table)

		table[1][j+1] = place_corner(pref, int(table[0][j+1]), int(table[1][j]), unseated)
		unseated.remove(table[1][j+1]) # remove right side element by value
		#print(table)
		#print(unseated)
		#print(table)

	#print(table) # Display seating chart

	# Give back the table
	return table


def place_bot_and_side(pref, cur_per, unseated, cut_off, goh):
	
	#print("-------------------------------------------------")
	options = []
	index = 0

	# The current person's favorite 4 people.
	cur_fav = np.argpartition(pref[cur_per], -4)[-4:]	# Their top 4 most liked people

	# Get the overlap between favorites and those unseated
	mask = np.isin(cur_fav, unseated)
	cur_fav_remaining = cur_fav[mask]
	
	#print("REMAINING ", cur_fav_remaining)

	cur_pref_val = pref[cur_per][cur_fav_remaining]	# Their corresponding pref values
	if cur_per < cut_off:	# Means they are a host
		cur_role = "host"
		goh = 0	# Host
	else:
		cur_role = "guest"
		goh = 1	# Guest

	#print("cur_p: {}\tcur_4_fav_people: {}\tcur_pref_vals: {}\tcur_role: {}".format(cur_per, cur_fav_remaining, cur_pref_val, cur_role))	
	if len(cur_fav_remaining) == 0:	# Empty list, then we go through everyone
		# Loop through all people
		cur_pref_val = pref[cur_per][unseated]
		for p in unseated:
			pref_for_cur = pref[p][cur_per]	# How person p feels about cur

			if p < cut_off:	# Means they are host
				p_role = "host"
				p_goh = 0
			else:	
				p_role = "guest"
				p_goh = 1

			#print ("p: {}\tp_pref_for_cur: {}\tp_role: {}".format(p, pref_for_cur, p_role))

			# Add the results
			cur_pref_val[index] += pref_for_cur	# How much p likes cur

			if goh != p_goh:				# Diff, therefore points
				cur_pref_val[index] += 2	# Add two points for opps
		
			index += 1	# Increment index

		# Display total of how much they like each other
		#print("cur_fav_people: {}\toverall_pref_vals: {}".format(cur_fav_remaining, cur_pref_val))
	
		# Best Choice
		#'''
		bc_index = np.argmax(cur_pref_val)
		best_choice = unseated[bc_index]
		#'''
		# Maybe take the top half of the remaining indexes - best points
		#best_choice = unseated[rand.randint(0, len(unseated) - 1)]	# Select random from unseated remaining

		#print("Seat p: {}".format(best_choice))
		return best_choice


	else:
		# Loop through cur's fav people and see how they feel about cur
		for p in cur_fav_remaining:
			pref_for_cur = pref[p][cur_per]	# How person p feels about cur

			if p < cut_off:	# Means they are host
				p_role = "host"
				p_goh = 0
			else:	
				p_role = "guest"
				p_goh = 1

			#print ("p: {}\tp_pref_for_cur: {}\tp_role: {}".format(p, pref_for_cur, p_role))

			# Add the results
			cur_pref_val[index] += pref_for_cur	# How much p likes cur

			if goh != p_goh:				# Diff, therefore points
				cur_pref_val[index] += 2	# Add two points for opps
		
			index += 1	# Increment index

		# Display total of how much they like each other
		#print("cur_fav_people: {}\toverall_pref_vals: {}".format(cur_fav_remaining, cur_pref_val))
	
		# Best Choice
		'''
		bc_index = np.argmax(cur_pref_val)
		best_choice = cur_fav_remaining[bc_index]
		'''
		best_choice = cur_fav_remaining[rand.randint(0, len(cur_fav_remaining) - 1)]	# Select random from top remaining

		#print("Seat p: {}".format(best_choice))
		return best_choice


def place_corner(pref, cur1, cur2, unseated):

	index = 0
	# The current person's favorite 4 people.
	cur1_fav = np.argpartition(pref[cur1], -4)[-4:]	# Their top 4 most liked people
	cur1_pref_val = pref[cur1][cur1_fav]	# Their corresponding pref values


	cur2_fav = np.argpartition(pref[cur2], -4)[-4:]	# Their top 4 most liked people
	cur2_pref_val = pref[cur2][cur2_fav]	# Their corresponding pref values

	mask = np.isin(cur1_fav, cur2_fav)
	cur_mutual_fav = cur1_fav[mask]
	#print("cur1: {}\tcur2: {}\tcur_mutual: {}".format(cur1_fav, cur2_fav, cur_mutual_fav))
	
	mask2 = np.isin(cur_mutual_fav, unseated)
	cur_mutual_fav_remaining = cur_mutual_fav[mask2]

	#print("remaining: {}\tlen: {}".format(cur_mutual_fav_remaining, len(cur_mutual_fav_remaining)))

	if len(cur_mutual_fav_remaining) == 0:	# If no mutual friends
		# Look through all unseated
		pref_totals = np.zeros(len(unseated))
		cur1_fav = pref[cur1][unseated]
		cur2_fav = pref[cur2][unseated]
		for p in unseated:
			pref_for_c1 = pref[p][cur1]
			pref_for_c2 = pref[p][cur2]

			pref_sum = cur1_fav[index] + cur2_fav[index] + pref_for_c1 + pref_for_c2
			pref_totals[index] = pref_sum
			index += 1


	else:

		pref_totals = np.zeros(len(cur_mutual_fav_remaining))
		cur1_fav = pref[cur1][cur_mutual_fav_remaining]
		cur2_fav = pref[cur2][cur_mutual_fav_remaining]
		for p in cur_mutual_fav_remaining:
			pref_for_c1 = pref[p][cur1]
			pref_for_c2 = pref[p][cur2]

			pref_sum = cur1_fav[index] + cur2_fav[index] + pref_for_c1 + pref_for_c2
			pref_totals[index] = pref_sum
			index += 1



	bc_index = np.argmax(pref_totals)
	best_choice = unseated[bc_index]
	return best_choice



# Return the role of the person - host or guest?
def role(person, num):
	''' Given a person and the number of people, identify their role.
		Then return True if they're a host and False if they're a guest.
	'''
	if person < int(num/2):	# Host if in the first half
		return True
	else:				# Not host ie a Guest
		return False


# Return scores for roles
def score_roles(p1, p2, num, opp):
	''' Given two people, the number of people, and a boolean opp variable.
		Determine the score to give based on role. Return 0 if the roles 
		are the same. If the roles are different, then return 1 if they
		are adjacent to one another and 2 if they're opposite of each other.
	'''
	if role(p1, num) == role(p2, num):	# If they're the same roles
		return 0
	else:						# If they're different roles
		if opp:					# If opposite of each other
			return 2
		else:					# They're next to each other
			return 1


# How much 1st person likes 2nd person - May be negative.
def preferance(p1, p2, pref):
	''' Given two people and the preferance matrix, determine how much the
		1st person likes the 2nd person. However, if given the transposed
		matrix, return the sum of how much both people like each other.
	'''
	return pref[int(p1)][int(p2)]	# return how much person 1 likes person 2


# Determine Scoring
'''
	- 1 point for every adjacent pair (seated next to 
		each other) of people with one a host and the 
		other a guest.
	- 2 points for every opposite pair (seated across
		from each other) of people with one a host and
		the other a guest.
	- h(p1, p2) + h(p2, p1) points for every adjacent 
		or opposite pair of people p1, p2.
'''
# Delete this
def scoring(s_tab, pref_tab, num_p):
	score = 0
	r_score = 0
	
	# For sanity check
	r_count = 0		# Check how many roles calculated - 13 for n=10
	s_count = 0 	# Check how many scores calculated - 26 for n=10


	# Loop through the table
	for i in range(2):						# Top and bottom
		for j in range (int(num_p/2)):		# Left to right
			# Deal with sitting across
			if i == 0:		#  Top of table
				# pref of i+1
				score += preferance(s_tab[i][j], s_tab[i+1][j], pref_tab)	# Get score from top to bottom
				# Check ROLE num_p/2 times for opposite pairs
				r_score += score_roles(s_tab[i][j], s_tab[i+1][j], num_p, True)	# opps - role once
				r_count += 1 # Sanity check

			else:	# Bottom of table
				# pref of i-1
				score += preferance(s_tab[i][j], s_tab[i-1][j], pref_tab)	# Get score from bottom to top

			s_count += 1	# Sanity check
		
			# Check ROLE for sitting adjacent (to the right) - num_p/2 -1
			if j < num_p/2 - 1:
				r_score += score_roles(s_tab[i][j], s_tab[i][j+1], num_p, False)	# adjs
				r_count += 1 # Sanity check


			# Deal with sitting on sides
			if j == 0 or j == int(num_p/2 - 1):	# at the corners
				if j == 0:	# left corner
					# Get pref of person right
					score += preferance(s_tab[i][j], s_tab[i][j+1], pref_tab)

				else:	# right corner
					# get pref of person left
					score += preferance(s_tab[i][j], s_tab[i][j-1], pref_tab)

				s_count += 1	# Sanity check

			else:	# Somewhere in the middle
				# Get pref of left and right	
				score += preferance(s_tab[i][j], s_tab[i][j-1], pref_tab)	# left
				score += preferance(s_tab[i][j], s_tab[i][j+1], pref_tab)	# right
				s_count += 2	# Sanity check

	'''
	print("Role Score: ", r_score)
	print("Role Count: ", r_count)
	print("Pref Score: ", score)
	print("Score Count: ", s_count)
	print("Final Score: ", score + r_score)
	#'''
	return score + r_score


def score_fast(s_tab, tran_pref_sum, num_p):
	''' More efficient scoring method, given a seated table,
		the transposed/summed preferance matrix, and the number of people,
		loop through both rows and get the roles and preferances of each pair.
		Return the final score of the table.
	'''
	score = 0
	r_score = 0
	
	for i in range(int(num_p/2)):
		score += tran_pref_sum[int(s_tab[0][i])][int(s_tab[1][i])]	# Score for sitting accross
		r_score += score_roles(s_tab[0][i], s_tab[1][i], num_p, True)	# opps - role once

		if i < int(num_p/2 - 1):	# Not on the last index
			score += tran_pref_sum[int(s_tab[0][i])][int(s_tab[0][i+1])]	# Score for top adjacent
			score += tran_pref_sum[int(s_tab[1][i])][int(s_tab[1][i+1])]	# Score for bot adjacent

			r_score += score_roles(s_tab[0][i], s_tab[0][i+1], num_p, False)	# Role adjs top
			r_score += score_roles(s_tab[1][i], s_tab[1][i+1], num_p, False)	# Role adjs bot

	'''
	print("score2: ", score)
	print("r_score2: ", r_score)
	print("-------------------------------")
	'''
	return score + r_score




if __name__== "__main__" :
	main(sys.argv)


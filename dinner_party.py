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
# Description: Project working with state spaces.
# Run with "python3 dinner_party.py"
# Installs "pip3 install <package>"
# Resources:
# 	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
#

import numpy as np
import random as rand

# Read the text file data into 2d array. Give back 2d array and num.
def read_data(data_file="data_insts/hw1-inst1.txt"):
	
	# Numpy read in my data - separate by space, skip row 1, all ints.	
	data = np.loadtxt(data_file, delimiter=" ", skiprows=1, dtype=int)
	num_p = len(data)
	#print(data)
	#print(num_p)
	
	return data, num_p


# Display the scoring in the correct format, then prepare to write out data
def display_scores(score, table, num_p):	
	print("Table Score: ", score)
	count = 1
	
	# Loop through the table
	for i in range(2):
		for j in range (int(num_p/2)):
			# Display current index
			print("p{} s{}".format(int(table[i][j]), count))	# Person# seat#
			count += 1
	

# Run the stuff
def main():
	pref, num_p = read_data() 						# Create Pref table and num people
	table_seats = np.zeros((2, int(num_p/2)))		# Table
	s_table = rand_agent(num_p, table_seats)		# Seated table
	table_score = scoring(s_table, pref, num_p)		# Score of seated table
	display_scores(table_score, s_table, num_p)		# Output of seated table score


# Randomly place people at the table for the standard.
def rand_agent(num_p, table):
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

	print(table) # Display seating chart

	# Give back the table
	return table	
	


# Return the role of the person - host or guest?
def role(person, num):
	if person < int(num/2):	# Host if in the first half
		return True
	else:				# Not host ie a Guest
		return False

# Return scores for roles
def score_roles(p1, p2, num, opp):
	if role(p1, num) == role(p2, num):	# If they're the same roles
		return 0
	else:						# If they're different roles
		if opp:					# If opposite of each other
			return 2
		else:					# They're next to each other
			return 1


# How much 1st person likes 2nd person - May be negative.
def preferance(p1, p2, pref):
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
def scoring(s_tab, pref_tab, num_p):
	score = 0
	r_score = 0

	# Loop through the table
	for i in range(2):
		for j in range (int(num_p/2)):
			# Deal with sitting across
			# if top of table
			if i == 0:
				# pref of i+1
				score += preferance(s_tab[i][j], s_tab[i+1][j], pref_tab)
				# Check ROLE num_p/2 times for opposite pairs
				r_score += score_roles(s_tab[i][j], s_tab[i+1][j], num_p, True)	# opps

			else:
				# pref of i-1
				score += preferance(s_tab[i][j], s_tab[i-1][j], pref_tab)

			# Check ROLE for sitting adjacent (to the right) - num_p/2 -1
			if j < num_p/2 - 1:
				r_score += score_roles(s_tab[i][j], s_tab[i][j+1], num_p, False)	# adjs

			# Deal with sitting on sides
			if j == 0 or j == int(num_p/2 - 1):	# at the corners
				if j == 0:	# left corner
					# Get pref of person right
					score += preferance(s_tab[i][j], s_tab[i][j+1], pref_tab)

				else:	# right corner
					# get pref of person left
					score += preferance(s_tab[i][j], s_tab[i][j-1], pref_tab)

			else:	# Somewhere in the middle
				# Get pref of left and right	
				score += preferance(s_tab[i][j], s_tab[i][j-1], pref_tab)	# left
				score += preferance(s_tab[i][j], s_tab[i][j+1], pref_tab)	# right

	#print("Role Score: ", r_score)
	#print("Pref Score: ", score)
	#print("Final Score: ", score + r_score)
	return score + r_score


if __name__== "__main__" :
	main()


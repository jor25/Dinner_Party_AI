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
	print(data)
	print(num_p)
	
	return data, num_p


# Run the stuff
def main():
	pref, num_p = read_data()
	table_seats = np.zeros((2,5))	# Table
	rand_agent(num_p, table_seats)
	
	pass


# Randomly place people at the table for the standard.
def rand_agent(num_p, table):
	unseated = list(range(num_p))	# Create list from 0 - num_p
	print(unseated)

	# Loop through the table
	for i in range(2):
		for j in range (int(num_p/2)):
			# Agent select random index from unseated list
			table[i][j] = unseated[rand.randint(0, len(unseated) - 1)]

			# Remove the specified value from unseated list
			unseated.remove(table[i][j]) # remove element by value
			print(unseated)
			print(table)

	# Give back the table
	return table	
	


# Return the role of the person - host or guest?
def role(person, num):
	if person < num/2:	# Host if in the first half
		return True
	else:				# Not host ie a Guest
		return False


# How much 1st person likes 2nd person - May be negative.
def preferance(p1, p2, pref):
	return pref[p1][p2]	# return how much person 1 likes person 2


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
def scoring(data):
	score = 0
	
	pass


if __name__== "__main__" :
	main()
	#read_data()


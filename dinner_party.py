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
# Date: 10-5-19
# Run with "python3 dinner_party.py"
# Installs "pip3 install <package>"

import numpy as np

# Read the text file data into 2d array. Give back 2d array and num.
def read_data(data_file="data_insts/hw1-inst1.txt"):
	
	# Numpy read in my data - separate by space, skip row 1, all ints.	
	data = np.loadtxt(data_file, delimiter=" ", skiprows=1, dtype=int)
	num_p = len(data)
	print(data)
	print(num_p)
	
	return data, num_p


def main():
	pass


# Return the role of the person - host or guest?
def role(person):
	pass


# How much 1st person likes 2nd person - May be negative.
def preferance(p1, p2):
	pass


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
	pass


if __name__== "__main__" :
	main()
	read_data()


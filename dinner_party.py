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
#

# Read the text file data into 2d array
def read_data():
	pass


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


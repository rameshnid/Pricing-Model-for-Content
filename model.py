
from scipy import stats
import scipy as sp
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from os import sys
import random
import math



########################################
#############INPUTS TO MODEL############
########################################

# Number of users in the simulation
N  =10000
# Number of regions in the simulation
M = 10

# M length list of probabilities of user belonging to specific regions 
prob_user_in_region = [0.2, 0.3, 0.5, 0, 0, 0, 0, 0, 0, 0]

# Cost in dollars for each of the M regions
cost_in_region = [5,5,5,5,5,5,5,5,5,5]

N_contentproviders = 25

# We assume that the number of videos on the system by each content provider could be anything from 1 to 100 videos with uniform probability and the length of a video could be between 1 to 150 minutes with some probability distribution 

max_videos_by_cp = 10
max_len_of_vid = 150

############################################
############END OF INPUTS####################
#############################################
#############################################


#Generate a list of N users

user_list = ['user' + str(i) for i in range(N)]


#Generating a list of M countries 

regions_list = ['region' + str(i) for i in range(M)]


# Function to select one of the items from choice_list with probabilities mentioned in prob_list

def gen_random_choice(choice_list,prob_list):
	if len(choice_list) != len(prob_list):
		print 'Error: Lengths of choice_list and prob_list dont match!'
		sys.exit() 
	
	range_list = [0]
	for i in xrange(len(prob_list)):
		range_list.append(prob_list[i]+range_list[i])
		
	rand_choice = random.random()
	return choice_list[len([choice for choice in range_list if rand_choice > choice]) - 1]
	
# user to region mapping
# the mapping is stored in a list of length equal to the size of the user base

geo_of_user = [gen_random_choice(regions_list,prob_user_in_region) for i in range(N)]


#print geo_of_user.count('region0')

#print user_list
#print regions_list
#print geo_of_user


# Generate a list of content providers

content_providers_list = ['cp' + str(i) for i in range(N_contentproviders)]

# Generate the geos of corresponding content providers

#content_providers_geo  = 

# Generating videos, video length and mapping with content providers
# vids_by_cp[i] = list of videos owned by content provider i

video_count = 0
vids_by_cp = []
for i in range(N_contentproviders):
	# generating number of videos the ith content provider has provided
	temp = random.randint(1,max_videos_by_cp)
	# generating video ids and their lenghts	
	vids_by_cp.append([])
	for j in range(temp):
		rand_len_vid = random.randint(1,max_len_of_vid)
		vids_by_cp[i].append(('video'+str(video_count),rand_len_vid))
		video_count = video_count + 1


# Generating a list of video space which is just a list of videos with their lengths
video_space = []
for i in range(len(vids_by_cp)):
	for j in range(len(vids_by_cp[i])):
		video_space.append(vids_by_cp[i][j])


print len(video_space), video_space

#print video_count

##################################################################
###########MODELING CONTENT CONSUMPTION PATTERNS##################
##################################################################

####Case 1: User consumes content with equal probabilities and his total consumption is around 900 minutes of video 

def f(x):
	a, b = x
	return b

def add(x,y):
	return x+y

mean_video_length = reduce(add, map(f,video_space))/len(video_space)

N_mins_consumed_by_user = 900

# generate binomial pmf centered at 

k = int(math.floor(N_mins_consumed_by_user/mean_video_length))
tries = range(2*k)
print stats.binom.pmf(tries,2*k-1,0.5)

#x = range(2*k + 1)
y = stats.binom.pmf(tries,2*k-1,0.5)
plt.plot(tries,y,"o",color="black")
plt.draw()
plt.show()



max_user_consumption_list = [int(math.floor(N_mins_consumed_by_user/mean_video_length)) for i in range(N)]

for i in range(N):
	max_user_consumption_list[i] = gen_random_choice(range(2*k),y)


###GENERATING CONSUMPTION DATA FOR USERS###

###GENERATING max_user_consumption_list[i] number of videos uniformly from video space and tagging it as consumption for user i
### Assuming the user is equally likely to consume all content (no bias towards regional content)

consumption_data = []

for i in range(N):
	consumption_data.append(random.sample(range(len(video_space)),max_user_consumption_list[i]))

#for i in range(10):
#	print consumption_data[i]
#	print max_user_consumption_list[i]
#	print "/n"

### UPDATING VIEW COUNTS and user lists on videos ###

view_counts = sp.zeros(len(video_space))
dollar_counts = sp.zeros(len(video_space))
video_views_userlist = []
for i in range(len(video_space)):
	video_views_userlist.append([])

for i in range(N):
	for k in consumption_data[i]:
		view_counts[k] += 1
		dollar_counts[k] += float(cost_in_region[int((geo_of_user[i])[-1:])])/len(consumption_data[i])
		(video_views_userlist[k]).append(i)
		
#print view_counts
#print video_views_userlist
print dollar_counts


#######CALCULATING YIELD ON VIDEOS#########

#video_yields

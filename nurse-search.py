import argparse
import numpy as np
import pandas as pd
import json


EARTH_RADIUS = 3959 #miles
DEGREE_TO_RAD = np.pi/180 #1/degrees


def lat_long_dist(lat1, lng1, lat2, lng2):
	# see https://en.wikipedia.org/wiki/Great-circle_distance
	lat1 = lat1*DEGREE_TO_RAD
	lng1 = lng1*DEGREE_TO_RAD
	lat2 = lat2*DEGREE_TO_RAD
	lng2 = lng2*DEGREE_TO_RAD
	return EARTH_RADIUS * np.arccos( np.sin(lat1)*np.sin(lat2) +
        np.cos(lat1)*np.cos(lat2)*np.cos(lng1-lng2) )
	

def main():

	# Handle the inputs
	parser = argparse.ArgumentParser(
		description='Find the Skilled Nursing Facilities near you by zipcode.'
		+' Try python nurse-search.py 35653 -sr 20')

	parser.add_argument('zip_code', type=int,
		help='The five-digit zip code around which to search.')	
	parser.add_argument('-sr', '--search_radius', type=int, 
		help='search radius in miles', default=10)
	parser.add_argument('-mr','--min_overall_rating', type=int,
		help='The minimum allowed overall quality rating.', default=1,
		choices = [1,2,3,4,5])	
		
	args = parser.parse_args()
			
	# read the data into pandas dataframes
	info = pd.read_csv('CSVs/ProviderInfo_Download.csv')
	centroids = pd.read_csv('CSVs/zip_code_centroids.csv',index_col='zip_code')
	
	# find the position of the given ZIP
	pos1 = centroids.loc[args.zip_code]
	
	# create a lat and long dataframe corresponding to the info df
	lat_lng = centroids.loc[info['ZIP']]
	lat_lng.index = range(len(lat_lng))

	# add distance from the given zip to the lat_lng dataframe
	def ll_dist(pos2):
		return lat_long_dist(pos1.lat, pos1.lng, pos2.lat, pos2.lng)
		
	lat_lng['dists'] = lat_lng.apply(ll_dist, axis=1)
	
	# Find the matches
	match_bool = ( ( (lat_lng['dists'] < args.search_radius)
	    | (info['ZIP'] == args.zip_code) ) 
		& (info['overall_rating'] >= args.min_overall_rating) )
	matches = info[match_bool]
	
	# Make a dataframe with the correct labels
	output = pd.DataFrame()
	output['name'] = matches['PROVNAME']
	output['address'] = matches['ADDRESS']
	output['city'] = matches['CITY']
	output['state'] = matches['STATE']
	output['zip_code'] = matches['ZIP']
	output['phone'] = matches['PHONE']
	output['overall_rating'] = matches['overall_rating']
	output['lat'] = lat_lng['lat']
	output['lng'] = lat_lng['lng']
	output['distance_miles'] = lat_lng['dists']
	#output['score'] = 
	
	# Sort the output df
	output = output.sort_values(['distance_miles', 'overall_rating'], 
		ascending=[1, 0])
		
	#print('Matches: ' + str(len(matches)))
	
	# Make a json structure for the ouput		
	return output.to_json(orient='records')


if __name__ == '__main__': 
	output = main()	
	print(output)
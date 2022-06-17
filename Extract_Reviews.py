! pip install -U googlemaps
import googlemaps
import time
import pandas as pd

states = ['Johor','Perlis','Kuala Lumpur','Melaka','Negeri Sembilan','Selangor','Sabah','Sarawak','Perak','Terengganu',
         'Kelantan','Labuan','Putrajaya','Johor','Pahang','Penang','Kedah']

gmaps = googlemaps.Client(key='AIzaSyCXW1W-4UH9HyZXqLNvhsxq6ec2d_1GWiI')

results = []
place_list = []

for state in states:
    params = {'query' : ['Psychiatry in ' + state]}
    
    for iter in range(3):
        time.sleep(2)
        places = gmaps.places(**params)
        results = [places['results'][i]['place_id'] for i in range(len(places['results']))]
        place_list += [gmaps.place(place_id = x) for x in results]
        unique_place = set([place_list[i]['result']['name'] for i in range(len(place_list))])
        if 'next_page_token' not in places:
            break
        params['page_token'] = places['next_page_token']


hold = []

for i in range(len(place_list)):
    name = place_list[i]['result']['name']
    address = place_list[i]['result']['adr_address']
    get_locality = place_list[i]['result']['address_components']
    for addr in get_locality:
        if addr['types'][0] == 'locality':
            locality = addr['long_name']
        if addr['types'][0] == 'administrative_area_level_1':
            state = addr['long_name']
    try:
        for j in range(len(place_list[i]['result']['reviews'])):
            text = place_list[i]['result']['reviews'][j]['text']
            
            if text:
                rating = place_list[i]['result']['reviews'][j]['rating']


                hold.append({'name' : name,'locality' : locality,'state' : state,
                             'address' : address,'rating' : rating,'text' : text})
    except:
        print(place_list[i]['result']['name'] + ' has no reviews.')
    
df = pd.DataFrame(hold)

df.to_csv('Extracted Reviews.csv')
df.to_excel('Extracted Reviews.xlsx')
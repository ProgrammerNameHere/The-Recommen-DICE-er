# Fetch the data via an API Script
# Import the necessary modules
import requests
import pandas as pd
import xmltodict
import time

# Define global Variables
url = 'https://boardgamegeek.com/xmlapi2/thing?'
max_ids_per_call = 20
counter = 0
form_values = {
    'id':'', # Specifies the id of the thing(s) to retrieve. To request multiple things with a single query, NNN can specify a comma-delimited list of ids. Maximum 20.
    #'type':'', # Specifies that, regardless of the type of thing asked for by id, the results are filtered by the THINGTYPE(s) specified. Multiple THINGTYPEs can be specified in a comma-delimited list.
    #'versions':'1', # Returns version info for the item.
    #'videos':'1', # Returns videos for the item.
    'stats':'1', # Returns ranking and rating stats for the item.
    #'historical':'1', # Not currently supported. Returns historical data over time. See page parameter.
    #'marketplace':'1', # Returns marketplace data.
    #'comments':'1', # Returns all comments about the item. Also includes ratings when commented. See page parameter.
    #'ratingcomments':'1', # Returns all ratings for the item. Also includes comments when rated. See page parameter. The ratingcomments and comments parameters cannot be used together, as the output always appears in the <comments> node of the XML; comments parameter takes precedence if both are specified. Ratings are sorted in descending rating value, based on the highest rating they have assigned to that item (each item in the collection can have a different rating).
    #'page':'1', # Defaults to 1, controls the page of data to see for historical info, comments, and ratings data.
    #'pagesize':'10', # Set the number of records to return in paging. Minimum is 10, maximum is 100.
    #'from':'', # Not currently supported.
    #'to':'' # Not currently supported.
}

# Load a list of all the games to update
all_games_ranked = pd.read_csv('../data/boardgames_ranks.csv').query('rank > 0')

# Extract the ID's of those games 
game_ids = all_games_ranked['id']

# Try to load an existing file if there is one
try:
    game_details = pd.read_csv('../data/game_details_raw.csv')
except FileNotFoundError:
    game_details = pd.DataFrame(columns=['game_id',
                                        #'alt_name', # maybe include, so the searching goes easier
                                        'description',
                                        #'yearpublished',
                                        'minplayers',
                                        'maxplayers',
                                        'community_best_with',
                                        'community_recommended_with',
                                        'playingtime',
                                        'minplaytime',
                                        'maxplaytime',
                                        'minage',
                                        #'community_minage',
                                        #'language_dependency', # superfluous? mostly focus on english games
                                        'boardgamecategories', 
                                        'boardgamemechanics',
                                        'boardgamefamilies',
                                        #'boardgameaccessories', # superfluous? probably has high correlation with the family and mechanics
                                        #'boardgameimplementations', # superfluous?
                                        'boardgamedesigners',
                                        'boardgameartists',
                                        #'boardgamepublishers', # superfluous?
                                        #'usersrated', # already in the dataset
                                        #'average', # already in the dataset
                                        #'bayesaverage', # already in the dataset
                                        #'ranks', # already in the dataset
                                        'stddev',
                                        'median',
                                        'owned',
                                        'trading',
                                        'wanting',
                                        'wishing',
                                        'numcomments',
                                        'numweights',
                                        'averageweight'
                                         ])

# Compare all the games to the games already present in the game_details_raw.csv file
game_ids_unupdated = list(map(str, set(game_ids) - set(game_details['game_id'].dropna().astype(int))))

# Helper function to extract the information from BGG
def _extract_details_from_link_element(link_element, detail_type):
    detail_list = []
    if type(link_element) == dict:
        if link_element['@type'] == detail_type:
            detail_list.append(item['@value'])
    else:
        for item in link_element:
            if item['@type'] == detail_type:
                detail_list.append(item['@value'])

    return ','.join(detail_list)
    pass # these infos are all in the same element and can occur multiple times. The different detail_types are: '

# Helper function to extract the information from BGG
def _extract_info_into_dataframe(df, item_dict):
    # save the info into a dictionary
    info = {
        'game_id': item_dict['@id'],
        #'name': item_dict[item], # included in dataset
        #'alt_name', # maybe include, so the searching goes easier
        'description': item_dict['description'],
        #'yearpublished': item_dict['yearpublished']['@value'], # already included in dataset
        'minplayers': item_dict['minplayers']['@value'],
        'maxplayers': item_dict['maxplayers']['@value'],
        'community_best_with': item_dict['poll-summary']['result'][0]['@value'],
        'community_recommended_with': item_dict['poll-summary']['result'][1]['@value'],
        'playingtime': item_dict['playingtime']['@value'],
        'minplaytime': item_dict['minplaytime']['@value'],
        'maxplaytime': item_dict['maxplaytime']['@value'],
        'minage': item_dict['minage']['@value'],
        #'community_minage': item_dict[item], # hassle to extract
        #'language_dependency': item_dict[item], # superfluous? mostly focus on english games
        'boardgamecategories': _extract_details_from_link_element(item_dict['link'], 'boardgamecategory'), 
        'boardgamemechanics': _extract_details_from_link_element(item_dict['link'], 'boardgamemechanic'),
        'boardgamefamilies': _extract_details_from_link_element(item_dict['link'], 'boardgamefamily'),
        #'boardgameaccessories': _extract_details_from_link_element(item_dict['link'], 'boardgameaccessory'), # superfluous? probably has high correlation with the family and mechanics
        #'boardgameimplementations': _extract_details_from_link_element(item_dict['link'], 'boardgameimplementation'), # superfluous?
        'boardgamedesigners': _extract_details_from_link_element(item_dict['link'], 'boardgamedesigner'),
        'boardgameartists': _extract_details_from_link_element(item_dict['link'], 'boardgameartist'),
        #'boardgamepublishers': _extract_details_from_link_element(item_dict['link'], 'boardgamepublisher'), # superfluous?
        #'usersrated': item_dict[item], # already in the dataset
        #'average': item_dict[item], # already in the dataset
        #'bayesaverage': item_dict[item], # already in the dataset
        #'ranks': item_dict[item], # already in the dataset
        'stddev': item_dict['statistics']['ratings']['stddev']['@value'],
        'median': item_dict['statistics']['ratings']['median']['@value'],
        'owned': item_dict['statistics']['ratings']['owned']['@value'],
        'trading': item_dict['statistics']['ratings']['trading']['@value'],
        'wanting': item_dict['statistics']['ratings']['wanting']['@value'],
        'wishing': item_dict['statistics']['ratings']['wishing']['@value'],
        'numcomments': item_dict['statistics']['ratings']['numcomments']['@value'],
        'numweights': item_dict['statistics']['ratings']['numweights']['@value'],
        'averageweight': item_dict['statistics']['ratings']['averageweight']['@value']
    }
    return info
    

# collect data from BGG
while game_ids_unupdated != []:
    # Get first 20 items and join with ','
    ids_to_update = ",".join(game_ids_unupdated[:max_ids_per_call])  
    # Remove them from the original list
    del game_ids_unupdated[:max_ids_per_call]  
    # update the API parameter to get the current id's
    form_values.update({'id':ids_to_update})
    # get the info from BGG
    response = requests.get(url, params=form_values)
    if response.status_code == 429:
        # print('Too many requests!', game_details.shape)
        counter +=1
        time.sleep(min(2 ** counter, 60))
    # save the info into the dataframe
    if response.status_code == 200:
        counter = 0
        info = xmltodict.parse(response.text)  
    else:
        game_ids_unupdated.extend(ids_to_update.split(','))
        continue
    for game in info['items']['item']:
            info_current_game = _extract_info_into_dataframe(game_details, game)
            df_current_game = pd.DataFrame(info_current_game, index = [int(info_current_game['game_id'])])
            game_details = pd.concat([game_details, df_current_game])

game_details.drop_duplicates(inplace=True)
game_details['game_id'] = game_details['game_id'].astype('int64')

cols_to_use = game_details.columns.difference(all_games_ranked.columns)
df = pd.merge(all_games_ranked, game_details[cols_to_use], left_on='id', right_on='game_id', suffixes=('',''))
df['description'] = df['description'].fillna('')
df.drop(columns=['id'], inplace=True)
df.to_csv('../data/game_details_raw.csv', index=False)

if df['community_best_with'].dtype == 'object':
    df['community_best_with'] = df['community_best_with'].str.extract('(\d+)').astype(float)
collective_columns = [#'boardgameartists',
                      'boardgamecategories',
                      #'boardgamedesigners',
                      #'boardgamefamilies',
                      'boardgamemechanics'
                      ]

df[collective_columns].fillna('')

for category in collective_columns:
    #print(category)
    df = df.join(df[category].str.get_dummies(sep=','), rsuffix=category)

df.to_csv('../data/game_details_cleaned.csv', index=False)
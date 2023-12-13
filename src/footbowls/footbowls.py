import pandas as pd
import requests
import os
from dotenv import load_dotenv

def footbowls(parameter, parameter_ids, season_id=None, **kwargs):
    """
    API wrapper for the footbowls API.

    Parameters:
    - parameter: str, the type of data to retrieve (e.g., 'teams', 'players', 'seasons', 'leagues').
    - parameter_ids: list of int, the list of IDs corresponding to the specified parameter.
    - season_id: int, the ID corresponding to the season (required for 'players' parameter).
    - kwargs: additional parameters for the API request.

    Returns:
    - pd.DataFrame: a DataFrame containing the retrieved data.
    """
    base_url = "https://api-football-v1.p.rapidapi.com/v3/"

    # Define endpoint based on the parameter
    endpoint = parameter

    load_dotenv()
    key = os.getenv('FOOTBALL_API_KEY')

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Include season ID if 'players' parameter is used
    if parameter == 'players' and season_id is not None:
        kwargs['season'] = str(season_id)

    # Make the API request for each ID
    finding_data = []
    for parameter_id in parameter_ids:
        # Add the current ID to the query string
        querystring = {**{'id': str(parameter_id)}, **kwargs}

        # Make the API request
        response = requests.get(base_url + endpoint, headers=headers, params=querystring)

        if response.status_code != 200:
            print(f"Error for ID {parameter_id}: {response.status_code}")
            continue

        # Parse JSON response
        finding = response.json()

        # Extract relevant data
        for queries in finding['response']:
            if parameter == 'teams':
                team_name = queries['team']['name']
                team_code = queries['team']['code']
                team_venue = queries['venue']['name']
                team_country = queries['team']['country']

                finding_data.append({
                    'Team Name': team_name,
                    'Team Code': team_code,
                    'Team Venue': team_venue,
                    'Country of Origin': team_country
                })
            elif parameter == 'players':
                player_name = queries['player']['firstname']+ ' ' + queries['player']['lastname']
                player_position = queries['statistics'][0]['games']['position']
                player_goals = queries['statistics'][0]['goals']['total']
                player_country = queries['player']['nationality']
                player_dob = queries['player']['birth']['date']
                player_team = queries['statistics'][0]['team']['name']

                finding_data.append({
                    'Player Name': player_name,
                    'Position': player_position,
                    'Total Goals': player_goals,
                    'Player Nationality': player_country,
                    'Player DOB': player_dob,
                    'Current Season Team': player_team
                })

    # Create a DataFrame
    df = pd.DataFrame(finding_data)

    return df
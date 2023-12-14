import pandas as pd
import requests
import os
from dotenv import load_dotenv

def get_teams(team_names=None, **kwargs):
    """
    API wrapper for the footbowls API to retrieve team information.

    Parameters:
    - team_names: string or list, the team name(s) to retrieve information.
    - kwargs: additional parameters for the API request.

    Returns a pandas dataframe containing the retrieved data.
    """
    base_url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    load_dotenv()
    key = os.getenv('FOOTBALL_API_KEY')

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Convert team names to a list
    if team_names is not None and not isinstance(team_names, list):
        team_names = [team_names]
    
    finding_data = []
    for team_name in team_names:
        querystring = {'name': team_name, **kwargs}

        response = requests.get(base_url, headers=headers, params=querystring)

        if response.status_code != 200:
            print(f"Error for team {team_name}: {response.status_code}")
            continue

        finding = response.json()

        for queries in finding['response']:
            team_id = queries['team']['id']
            team_name = queries['team']['name']
            team_code = queries['team']['code']
            team_venue = queries['venue']['name']
            team_country = queries['team']['country']

            finding_data.append({
                'Team ID': team_id,
                'Team Name': team_name,
                'Team Code': team_code,
                'Team Venue': team_venue,
                'Country of Origin': team_country,
                
            })

    df = pd.DataFrame(finding_data)

    return df

def get_players(parameter_id, season_id=None, **kwargs):
    """
    API wrapper for the footbowls API to get player information.

    Parameters:
    - parameter_id: string or list, the player ID(s) to retrieve information.
    - season_id: int, the ID corresponding to the season (required for 'players' parameter).
    - kwargs: additional parameters for the API request.

    Returns a pandas dataframe containing the retrieved data.
    """
    base_url = "https://api-football-v1.p.rapidapi.com/v3/players"

    load_dotenv()
    key = os.getenv('FOOTBALL_API_KEY')

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    finding_data = []
    for player_id in parameter_id:
        querystring = {**{'id': str(player_id)}, **kwargs}

        if season_id is not None:
            querystring['season'] = str(season_id)

        response = requests.get(base_url, headers=headers, params=querystring)

        if response.status_code != 200:
            print(f"Error for player ID {player_id}: {response.status_code}")
            continue

        finding = response.json()

        for queries in finding['response']:
            player_name = queries['player']['firstname'] + ' ' + queries['player']['lastname']
            player_position = queries['statistics'][0]['games']['position']
            player_goals = queries['statistics'][0]['goals']['total']
            player_country = queries['player']['nationality']
            player_dob = queries['player']['birth']['date']
            player_team = queries['statistics'][0]['team']['name']

            finding_data.append({
                'Player Name': player_name,
                'Position': player_position,
                'Total Goals': player_goals,
                'Nationality': player_country,
                'Player DOB': player_dob,
                'Current Season Team': player_team
            })

    df = pd.DataFrame(finding_data)

    return df
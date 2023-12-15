import pandas as pd
import requests
import os
from dotenv import load_dotenv

def get_teams(team_names=None, **kwargs):
    """
    Function to obtain team information from the API-Football API.

    Parameters
    ----------
    team_names : str or list, optional
        The team name(s) to retrieve information.
    kwargs : dict, optional
        Additional parameters for the API request.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the retrieved data.

    Examples
    --------
    Example usage for 'get_teams' function with team names:

    >>> team_names = ['Liverpool', 'Real Madrid', 'Manchester United']
    >>> teams_df = get_teams(team_names=team_names)
    >>> print(teams_df)

       Team ID          Team Name Team Code                 Team Venue Country of Origin  
    0       40          Liverpool       LIV                    Anfield          England  
    1      541        Real Madrid       REA  Estadio Santiago Bernabéu           Spain  
    2       33  Manchester United       MUN               Old Trafford          England
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
    Function to obtain player information from the API-Football API.

    Parameters
    ----------
    parameter_id : str or list
        The player ID(s) to retrieve information. (Full player ID list available on the API-Football website)
    season_id : int, optional
        The ID corresponding to the season (required for 'players' parameter). Season ID is referring to the year (i.e. 2014, 1997, etc.)
    kwargs : dict, optional
        Additional parameters for the API request.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the retrieved data.

    Examples
    --------
    Example usage for 'get_players' function with player IDs and Season ID 2022:

    >>> player_ids = [77, 56, 290]
    >>> players_df = get_players(player_ids, 2014)
    >>> print(players_df)

       Player Name        Position  Total Goals  Nationality  Player DOB  \
    0  Mats Rits        Midfielder            2      Belgium    1993-07-18   
    1  Antoine Griezmann  Attacker           22      France     1991-03-21   
    2  Virgil van Dijk    Defender            4      Netherlands 1991-07-08   

    Current Season Team  
    0         KV Mechelen  
    1         Atletico Madrid  
    2         Celtic
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

def cleague(country):
    """
    Function to obtain a list of football leagues for a specific country from the API-Football API.

    Parameters
    ----------
    - country (str): The name of the country for which you want to retrieve football leagues.

    
    Returns
    -------
    - pd.DataFrame: A DataFrame containing a list of football leagues for the specified country.

    
    Examples
    --------
    Example usage for 'cleague' function with country name 'albania':

    >>>> country_name = 'albania'
    >>>> leagues_df = cleague(country_name)

    >>>> if not leagues_df.empty:
    >>>> print(leagues_df)
        List of Leagues in albania League ID
    0     2nd Division - Group B    (513,)
    1     2nd Division - Group A    (512,)
    2                  Superliga    (310,)
    3               1st Division    (311,)
    4                        Cup    (707,)
    5                  Super Cup    (708,)
    6   2nd Division - Play-offs    (978,)
    """

    base_url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    load_dotenv()
    key = os.getenv('FOOTBALL_API_KEY')
    
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    querystring = {'country': country}
    response = requests.get(base_url, headers=headers, params=querystring)
    finding = response.json()

    if 'response' in finding:
        finding_data = []
        for league_info in finding['response']:
            league_id = league_info['league']['id'],
            league_name = league_info['league']['name']
            
            finding_data.append({
                f"List of Leagues in {country}": league_name,
                'League ID': league_id
            })

        df = pd.DataFrame(finding_data)
        return df
    else:
        print(f"No leagues found for the country: {country}")
        return pd.DataFrame()
import pandas as pd
import pytest
from footbowls import footbowls

@pytest.fixture
def sample_team_names():
    return ['Liverpool', 'Real Madrid', 'Manchester United']

def test_get_teams(sample_team_names):
    teams_df = footbowls.get_teams(team_names=sample_team_names)
    assert isinstance(teams_df, pd.DataFrame)

    expected_columns = ['Team ID', 'Team Name', 'Team Code', 'Team Venue', 'Country of Origin']
    assert all(column in teams_df.columns for column in expected_columns)


@pytest.fixture
def sample_player_ids():
    return [77, 56, 290]

@pytest.fixture
def sample_season_id():
    return 2014

def test_get_players(sample_player_ids, sample_season_id):
    players_df = footbowls.get_players(sample_player_ids, sample_season_id)
    assert isinstance(players_df, pd.DataFrame)

    expected_columns = ['Player Name', 'Position', 'Total Goals', 'Nationality', 'Player DOB', 'Current Season Team']
    assert all(column in players_df.columns for column in expected_columns)

@pytest.fixture
def sample_country():
    return 'England'

def test_cleague(sample_country):
    cleague_df = footbowls.cleague(sample_country)
    assert isinstance(cleague_df, pd.DataFrame)

    expected_columns = [f"List of Leagues in {sample_country}", 'League ID']
    assert all(column in cleague_df.columns for column in expected_columns)

if __name__ == "__main__":
    pytest.main()


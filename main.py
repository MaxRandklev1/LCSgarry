import pandas as pd
import requests
import openai

openai.api_key = "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"
class EsportsDataAnalyzer:
    def __init__(self, api_key, file_path):
        self.api_key = api_key
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        """
        Load the esports data from a CSV file.
        """
        return pd.read_csv(self.file_path)

    def prepare_data(self):
        """
        Prepare the data by calculating opposing teams.
        """
        team_pairs_df = self.df[['gameid', 'teamname']].drop_duplicates().groupby('gameid')['teamname'].apply(list).reset_index()
        team_pairs_df = team_pairs_df[team_pairs_df['teamname'].apply(len) == 2]
        team_pairs_df['team1'] = team_pairs_df['teamname'].apply(lambda x: x[0])
        team_pairs_df['team2'] = team_pairs_df['teamname'].apply(lambda x: x[1])
        team_pairs_df.drop('teamname', axis=1, inplace=True)

        self.df = self.df.merge(team_pairs_df, on='gameid', how='inner')
        self.df['opposing_team'] = self.df.apply(lambda row: row['team2'] if row['teamname'] == row['team1'] else row['team1'], axis=1)

    def calculate_average_kills(self):
        """
        Calculate average kills for each player against each opposing team.
        """
        return self.df.groupby(['playername', 'opposing_team'])['kills'].mean().reset_index()

    def player_performance_against_team(self, player_name, team_name):
        """
        Get a specific player's performance against a specific team.
        """
        return self.df[(self.df['playername'] == player_name) & (self.df['opposing_team'] == team_name)]

    def send_to_gpt(self, data):
        """
        Send data to your GPT model using the API key.
        """
        url = "your_gpt_model_api_endpoint"  # Replace with your API endpoint
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

# Example usage
api_key = "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"  # Replace with your actual API key
file_path = '*.csv'  # Replace with the path to your file
analyzer = EsportsDataAnalyzer(api_key, file_path)
analyzer.prepare_data()
average_kills_df = analyzer.calculate_average_kills()

# Get specific player performance
performance = analyzer.player_performance_against_team('Hery', 'Team WE')
response = analyzer.send_to_gpt(performance)
print(response)

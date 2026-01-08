import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import leaguedashteamstats
from check_player_trend import check_player_trend

def calculate_ewma(all_season_scores, span):
    clean_scores = all_season_scores[::-1]
    alpha = 2 / (span + 1)
    ewma = clean_scores[0]
    for score in clean_scores[1:]:
        ewma = alpha * score + (1 - alpha) * ewma
    return ewma

def predict_points(player_name, opposing_team, is_home):
    player_info = check_player_trend(player_name, is_home)
    stats = leaguedashteamstats.LeagueDashTeamStats(season='2025-26', per_mode_detailed='PerGame', measure_type_detailed_defense='Base')
    df = stats.get_data_frames()[0]
    df['OPP_PTS'] = df['PTS'] - df['PLUS_MINUS']
    opp_pts = df.loc[df['TEAM_NAME'].str.contains(opposing_team, case=False), 'OPP_PTS'].iloc[0]
    factor = opp_pts / df['OPP_PTS'].mean()
    baseline = 0.6 * calculate_ewma(player_info['all_point_totals'], 10) + 0.4 * player_info["season_ppg"]
    #print("factor: ", factor)
    #print("baseline: ", baseline)
    return factor * baseline


if __name__=="__main__":
    print(round(predict_points("Giannis Antetokounmpo", "Warriors", False), 1))
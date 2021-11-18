from utils import *

teams = ['A', 'B']
zones = ['two', 'non_corner_three', 'corner_three']
metrics = ['attempt_pct', 'efg_pct']

def main(team, zone, metric):
    data_df = pd.read_csv('./dat.csv')
    data_df['zone'] = make_zones_list(data_df)
    shots_df = make_shots_df(data_df)
    final_df = add_percentage_cols(shots_df)
    return round(final_df.T[('Team '+team, zone)][metric], 3)
    

if __name__ == '__main__':
    for team in teams:
        for metric in metrics:
            for zone in zones:
                print(team, zone, metric, main(team, zone, metric))
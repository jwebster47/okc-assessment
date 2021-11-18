import pandas as pd

def determine_magnitude(x, y):
    return (x**2+y**2)**(1/2)

def determine_zone(x, y):
    magnitude = determine_magnitude(x, y)
    # assumes non-negative x and y values
    if y <= 7.8:
        if x > 22:
            return 'corner_three'
        elif x <= 22:
            return 'two'
        else:
            raise Exception
    else: # y > 7.8
        if magnitude > 23.75:
            return 'non_corner_three'
        elif magnitude <= 23.73:
            return 'two'
        else:
            raise Exception
            
def make_zones_list(df):
    zones = []
    for _, row in df.iterrows():
        x = abs(row['x'])
        y = abs(row['y'])
        zones.append(determine_zone(x,y))
    return zones

def make_shots_df(data_df):
    attempts = data_df.groupby(['team','zone'])['fgmade'].count().rename('attempts')
    made = data_df.groupby(['team','zone'])['fgmade'].sum().rename('made')
    return pd.DataFrame([attempts, made]).T

def add_percentage_cols(shots_df):
    old_index = shots_df.index
    old_rows = []
    for _, row in shots_df.iterrows():
        if 'two' in row.name[1]:
            efg = row[1]/row[0]
        elif 'three' in row.name[1]:
            efg = 1.5*row[1]/row[0]
        else:
            raise Exception
        if 'Team A' in row.name[0]:
            total_attempts = shots_df.groupby('team')['attempts'].sum()['Team A']
        elif 'Team B' in row.name[0]:
            total_attempts = shots_df.groupby('team')['attempts'].sum()['Team B']
        else:
            raise Exception
        efg_val = pd.Series(efg, index=['efg_pct'])
        dist_val = pd.Series(row[0]/total_attempts, index=['attempt_pct'])
        old_rows.append(row.append(dist_val).append(efg_val))
    return pd.DataFrame(old_rows, index=old_index)
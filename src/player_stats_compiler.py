import pandas as pd
import json
import os

def compile_player_stats():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    deliveries_path = os.path.join(base_dir, "data", "deliveries.csv")
    output_path = os.path.join(base_dir, "data", "player_stats.json")
    
    if not os.path.exists(deliveries_path):
        print("Error: deliveries.csv not found! Please run `python src/data_updater.py` first.")
        return
        
    print("Loading ball-by-ball deliveries...")
    df = pd.read_csv(deliveries_path)
    stats = {}
    
    # 1. Batting Metrics
    print("Aggregating Batting Stats...")
    batting = df.groupby('batsman').agg(
        total_runs=('batsman_runs', 'sum'), 
        balls_faced=('batsman_runs', 'count')
    ).reset_index()
    batting['strike_rate'] = (batting['total_runs'] / batting['balls_faced'] * 100).round(2)
    
    # 2. Bowling Metrics
    print("Aggregating Bowling Stats...")
    runs_conceded = df.groupby('bowler').agg(runs_conceded=('total_runs', 'sum')).reset_index()
    
    # Identify strictly legal deliveries to calculate Economy accurately
    df['is_legal'] = ~df['extras_type'].isin(['wides', 'noballs'])
    legal_balls = df[df['is_legal']].groupby('bowler').size().reset_index(name='legal_balls')
    
    # Identify wickets (excluding non-bowler accredited wickets)
    wickets_df = df.dropna(subset=['dismissal_kind'])
    wickets_df = wickets_df[~wickets_df['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field'])]
    wickets = wickets_df.groupby('bowler').size().reset_index(name='wickets')
    
    # Combine Bowling Metrics
    bowling = pd.merge(runs_conceded, legal_balls, on='bowler', how='left')
    bowling = pd.merge(bowling, wickets, on='bowler', how='left').fillna(0)
    
    bowling['economy'] = (bowling['runs_conceded'] / (bowling['legal_balls'] / 6)).round(2)
    bowling.loc[bowling['legal_balls'] == 0, 'economy'] = 0.0
    
    # 3. Serialization
    print("Merging metrics into compressed JSON payload...")
    b_dict = batting.set_index('batsman').to_dict(orient='index')
    bw_dict = bowling.set_index('bowler').to_dict(orient='index')
    
    all_players = set(b_dict.keys()).union(set(bw_dict.keys()))
    for player in all_players:
        b = b_dict.get(player, {})
        w = bw_dict.get(player, {})
        
        runs = int(b.get('total_runs', 0))
        wkts = int(w.get('wickets', 0))
        
        # Omit generic zero-data entries
        if runs > 0 or wkts > 0:
            stats[str(player)] = {
                "runs": runs,
                "sr": float(b.get('strike_rate', 0.0)),
                "wickets": wkts,
                "econ": float(w.get('economy', 0.0))
            }
            
    with open(output_path, 'w') as f:
        json.dump(stats, f)
        
    print(f"Successfully compiled {len(stats)} players into {output_path}")
    print(f"Memory Footprint: {os.path.getsize(output_path) / 1024:.2f} KB")

if __name__ == "__main__":
    compile_player_stats()

import pandas as pd
import numpy as np
import os

def generate_mock_data():
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    teams = ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals', 'Sunrisers Hyderabad']
    venues = ['Wankhede Stadium', 'M. Chinnaswamy Stadium', 'Eden Gardens', 'Chepauk', 'Arun Jaitley Stadium']
    
    data = []
    # Generate 1000 mock matches
    for i in range(1000):
        team1, team2 = np.random.choice(teams, 2, replace=False)
        toss_winner = np.random.choice([team1, team2])
        toss_decision = np.random.choice(['bat', 'field'])
        venue = np.random.choice(venues)
        
        # Simple heuristic: The toss winner has a slightly higher chance of winning
        base_prob = np.random.rand()
        if base_prob > 0.4:
            winner = toss_winner
        else:
            winner = team1 if toss_winner == team2 else team2
            
        data.append({
            'id': i,
            'season': np.random.randint(2008, 2024),
            'city': venue.split()[0],
            'team1': team1,
            'team2': team2,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision,
            'venue': venue,
            'winner': winner
        })
        
    df = pd.DataFrame(data)
    
    output_path = os.path.join(os.path.dirname(__file__), "matches.csv")
    df.to_csv(output_path, index=False)
    print(f"Mock data successfully generated at {output_path}")

if __name__ == "__main__":
    generate_mock_data()

import csv
import random
import uuid
import numpy as np

def generate_mock_data(num_entries=1000):
    # Modified boost multiplier distribution
    def custom_boost_multiplier():
        # Generate boost multipliers with controlled distribution
        random_value = random.random()
        if random_value < 0.8:  # 80% chance of 1.0x
            return 1.0
        elif random_value < 0.98:  # 18% chance of intermediate multipliers
            return random.choice([1.1, 1.25, 1.5, 2.0])
        else:  # 2% chance of 5.0x
            return 5.0
    
    mock_data = []
    
    for _ in range(num_entries):
        stake_amount = round(random.uniform(1, 10), 2)
        stake_duration = round(random.uniform(0, 23), 2)
        boost_multiplier = custom_boost_multiplier()
        
        # Calculate basicGold and totalGold
        basic_gold = round(stake_amount * stake_duration * 1000, 2)
        total_gold = round(basic_gold * boost_multiplier, 2)
        
        # Calculate paidBNB
        paid_bnb = round(basic_gold * 0.00001, 4)
        
        entry = {
            "id": str(uuid.uuid4()),  # Unique identifier
            "stake_amount": stake_amount,
            "stake_duration": stake_duration,
            "boost_multiplier": boost_multiplier,
            "initial_staking": 0,
            "basicGold": basic_gold,
            "totalGold": total_gold,
            "paidBNB": paid_bnb
        }
        mock_data.append(entry)
    
    return mock_data

# Generate mock data
mock_data = generate_mock_data()

# Save to CSV file
with open('mock_staking_data.csv', 'w', newline='', encoding='utf-8') as f:
    # Define the CSV headers
    fieldnames = ['id', 'stake_amount', 'stake_duration', 'boost_multiplier', 
                  'initial_staking', 'basicGold', 'totalGold', 'paidBNB']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    # Write headers
    writer.writeheader()
    
    # Write data rows
    writer.writerows(mock_data)

# Print some statistics for verification
print(f"Total entries: {len(mock_data)}")
print("\nSample Entry:")
print(mock_data[0])
print("\nStatistics:")
stakes = [entry['stake_amount'] for entry in mock_data]
durations = [entry['stake_duration'] for entry in mock_data]
basic_golds = [entry['basicGold'] for entry in mock_data]
total_golds = [entry['totalGold'] for entry in mock_data]
paid_bnbs = [entry['paidBNB'] for entry in mock_data]
boosts = [entry['boost_multiplier'] for entry in mock_data]

print(f"Stake Amount - Min: {min(stakes)}, Max: {max(stakes)}, Avg: {sum(stakes)/len(stakes):.2f}")
print(f"Stake Duration - Min: {min(durations)}, Max: {max(durations)}, Avg: {sum(durations)/len(durations):.2f}")
print(f"Basic Gold - Min: {min(basic_golds)}, Max: {max(basic_golds)}, Avg: {sum(basic_golds)/len(basic_golds):.2f}")
print(f"Total Gold - Min: {min(total_golds)}, Max: {max(total_golds)}, Avg: {sum(total_golds)/len(total_golds):.2f}")
print(f"Paid BNB - Min: {min(paid_bnbs)}, Max: {max(paid_bnbs)}, Avg: {sum(paid_bnbs)/len(paid_bnbs):.4f}")

print("\nBoost Multiplier Distribution:")
boost_distribution = {}
for boost in [1.0, 1.1, 1.25, 1.5, 2.0, 5.0]:
    count = boosts.count(boost)
    percentage = (count / len(boosts)) * 100
    boost_distribution[boost] = f"{count} ({percentage:.2f}%)"
print(boost_distribution)

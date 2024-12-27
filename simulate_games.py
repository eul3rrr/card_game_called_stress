from card_game import play_game

def simulate_games(num_simulations):
    import pandas as pd

    all_results = []

    for i in range(num_simulations):
        result = play_game()
        result_flat = {
            "winner": result["winner"],
            "total_rounds": result["total_rounds"],
            "rounds_since_last_stuck": result["rounds_between_stuck"][-1] if result["rounds_between_stuck"] else 0,
            "average_rounds_between_stuck": sum(result["rounds_between_stuck"]) / len(result["rounds_between_stuck"]) if result["rounds_between_stuck"] else 0,
            "total_stuck_events": result["total_stuck_events"]
        }
        all_results.append(result_flat)

    df = pd.DataFrame(all_results)

    # Add averages as a new row
    averages = {col: df[col].mean() if df[col].dtype != 'object' else 'Average' for col in df.columns}
    df = pd.concat([df, pd.DataFrame([averages])], ignore_index=True)

    df.to_csv("simulation_results.csv", index=False)
    print("Simulation completed. Results saved to 'simulation_results.csv'.")
    return df

if __name__ == "__main__":
    num_simulations = 10000  # Set the number of games to simulate
    simulate_games(num_simulations)
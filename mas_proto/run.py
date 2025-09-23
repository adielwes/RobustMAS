import numpy as np
import pandas as pd
from model import RescueModel

# Base profiles
MonitorRigoroso = dict(attention_radius=2, monitor_interval=1, comm_prob=0.2, wm_decay=0.01)
Comunicador     = dict(attention_radius=2, monitor_interval=3, comm_prob=0.6, wm_decay=0.02)
Explorador      = dict(attention_radius=3, monitor_interval=2, comm_prob=0.1, wm_decay=0.03)

def run_experiment(config_name, team_profiles, runs=20, fail_prob=0.02, seed=42):
    rows = []
    rng = np.random.default_rng(seed)
    for r in range(runs):
        m = RescueModel(
            width=20, height=20,
            n_agents=len(team_profiles),
            n_victims=12, n_hints=10,
            team_profiles=team_profiles,
            fail_prob=fail_prob,
            max_steps=400,
            seed=int(rng.integers(0, 1_000_000))
        )
        done = False
        while not done:
            done = m.step()

        df = m.datacollector.get_model_vars_dataframe()
        # métricas finais
        final = df.iloc[-1].to_dict()
        final.update({
            "config": config_name,
            "steps": m.step_count
        })
        rows.append(final)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    # Settings: homogeneous vs heterogeneous
    homog_monitor = [MonitorRigoroso]*6
    homog_comms   = [Comunicador]*6
    heterog_misto = [MonitorRigoroso, Comunicador, Explorador, MonitorRigoroso, Comunicador, Explorador]

    df1 = run_experiment("homog_monitor", homog_monitor)
    df2 = run_experiment("homog_comms", homog_comms)
    df3 = run_experiment("heterog_misto", heterog_misto)

    df = pd.concat([df1, df2, df3], ignore_index=True)
    print(df.groupby("config")[["success", "coverage", "rescued", "alive_agents", "steps"]].mean().round(3))
    # Saves raw results
    df.to_csv("results.csv", index=False)
    print("\nResults saved in results.csv")

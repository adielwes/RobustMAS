# BehavioralMAS: Multi-Agent Teams with Stable Behavioral Profiles

This project is a simple prototype of a **multi-agent system** using [Mesa](https://mesa.readthedocs.io/en/stable/), where agents are differentiated by **stable behavioral profiles** (parameters that affect attention, memory, communication, and monitoring).  
The goal is to compare **homogeneous teams** vs **heterogeneous teams** in **search and rescue** scenarios, evaluating efficiency, coverage, and robustness against failures.

---

## 🔎 Concept

Each agent is configured with a **behavioral profile**, defined by:

- `attention_radius`: perception/attention radius.  
- `monitor_interval`: frequency of rechecking objectives.  
- `comm_prob`: probability of communicating with neighbors.  
- `wm_decay`: decay rate of working memory.  

Implemented profiles:
- **RigorousMonitor** → strong focus on monitoring, little communication.  
- **Communicator** → frequently shares information, but monitors less.  
- **CautiousExplorer** → larger attention radius, less communication.   

---

## 📂 Code Structure

```yaml
mas_proto/
│── agents.py       # Definition of agents and profiles
│── model.py        # MAS model, 2D grid, metrics collection
│── run.py          # Main script to run experiments
│── requirements.txt
│── setup_env.sh    # Script to create virtual environment
```

---

## ⚙️ Installation

### 1. Create virtual environment
```bash
chmod +x setup_env.sh
./setup_env.sh
```

Activate the environment:
```bash
source venv_mas/bin/activate
```

### 2. (Alternative) Install via requirements.txt
```bash
pip install -r requirements.txt
```

### ▶️ Execution

Run the main experiments:

```bash
python run.py
```

The script runs 20 simulations for each configuration:

- `homog_monitor`: 6 agents with the RigorousMonitor profile
- `homog_comms`: 6 agents with the Communicator profile
- `heterog_misto`: 2 of each profile (RigorousMonitor, Communicator, CautiousExplorer)

Average results are printed in the terminal and saved in `results.csv`.

### 📊 Collected Metrics

- `success` → fraction of victims rescued (the higher, the better).
- `coverage` → fraction of the grid visited by at least one agent.
- `rescued` → number of victims rescued.
- `alive_agents` → agents still active at the end of the simulation (considering failures).
- `steps` → number of steps until mission completion (the lower, the better).


### 📜 License

This project is distributed under the **GNU General Public License v3.0 (GPL-3.0)**.  
You are free to use, modify, and distribute this software, provided that any derivative work is also licensed under the GPL-3.0 and proper credit is given to the original author.

---

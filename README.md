

## PetriRL Intralogistics (`petrirl-fms-v0`)  
## Framework Overview  

![Framework](https://github.com/Sofiene-Uni/Intralogistics/blob/main/framework.png)  

---
The **PetriRL Intralogistics** environment is part of the PetriRL package, it focuses on **Flexible Manufacturing Systems** with intralogistics challenges such as:  

- **AGV Scheduling** – Coordinating multiple automated guided vehicles.  
- **Tool-Sharing Optimization** – Managing shared tools across jobs and machines.  
- **Dynamic Job Shop Scheduling** – Adapting workflows under uncertainty and disruptions. 
- **Model-Based RL Rollouts:** Used to determine optimal AGV positioning, further improving operational efficiency. 

### Key Features  

- **Colored-Timed Petri Nets (CTPNs):**  
  Capture workflows, timing constraints, and resource dependencies. Enable **dynamic action masking** to eliminate infeasible choices.  

- **Actor-Critic Reinforcement Learning:**  
  Integrates model-based RL with actor-critic methods for adaptive scheduling and lookahead strategies for AGV/tool utilization.  

- **Gym-Compatible Environment:**  
  Fully compatible with OpenAI Gym for seamless integration into RL pipelines.  

- **Benchmarks:**  
  Includes classical **Taillard instances** and a newly developed **large-scale intralogistics benchmark** inspired by real-world manufacturing systems.  

- **Performance:**  
  Matches or outperforms classical optimization on makespan while achieving faster computation times.  

---
## Installation  

```bash
pip install petrirl

# PetriRL: Advanced Scheduling with Petri Nets and Reinforcement Learning  

**PetriRL** is a framework that integrates the structural modeling power of **Petri Nets** with the adaptability of **reinforcement learning (RL)** to solve dynamic scheduling problems in **Flexible Manufacturing Systems (FMS)**.  

By leveraging **Colored-Timed Petri Nets (CTPNs)** and **actor-critic RL**, PetriRL achieves improved **makespan performance**, **adaptability to dynamic environments**, and **computational efficiency** compared to traditional scheduling methods.  

---

## Why PetriRL?  

Flexible Manufacturing Systems require adaptive resource management to handle uncertainty, shared resources, and complex workflows. PetriRL provides:  

- **Dynamic Action Masking** – Reduces the RL action space using Petri Net token distributions, improving sample efficiency and stability.  
- **Policy-Based RL** – Supports knowledge transfer, adaptability to unseen problems, and near real-time scheduling decisions.  
- **Explainability** – Petri Net semantics and token flows provide transparent insights into decision-making.  
- **Scalability** – Modular Petri Net design supports large-scale manufacturing systems.  

---

## PetriRL Intralogistics (`petrirl-fms-v0`)  

The **PetriRL Intralogistics** environment focuses on **Flexible Manufacturing Systems** with intralogistics challenges such as:  

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

## Framework Overview  

![Framework](https://github.com/Sofiene-Uni/Intralogistics/blob/main/framework.png)  

---

## Installation  

```bash
pip install petrirl

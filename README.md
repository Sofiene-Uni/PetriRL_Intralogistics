# PetriRL: Advanced Scheduling with Petri Nets and Reinforcement Learning

**PetriRL** combines the formalism of Petri Nets with reinforcement learning to tackle dynamic scheduling in Flexible Manufacturing Systems (FMS). It offers a reproducible framework for research and industrial applications, demonstrating improved makespan and computational efficiency using **Colored-Timed Petri Nets (CTPNs)** and **actor-critic reinforcement learning**. 

## PetriRL Intralogistics

`PetriRL_intralogistics` is one of the environments provided in the PetriRL package. It focuses on **Flexible Manufacturing Systems (FMS)** and is designed to handle complex intralogistics challenges, including **AGV scheduling**, **tool-sharing optimization**, and dynamic job shop scheduling.  

Our approach combines the structural modeling power of Petri nets with the dynamic decision-making of policy-based reinforcement learning. Key aspects include:

- **Dynamic Action Masking:** Token distributions in the Petri net generate dynamic masks that reduce the RL search space, improve sample efficiency, aid credit assignment, and mitigate the combinatorial curse.
- **Policy-Based Reinforcement Learning:** Enhances knowledge retention and transferability, allowing the agent to generalize to unseen problems and make near real-time decisions.
- **Explainability:** Graphical semantics and token flows provide insights into scheduling decisions.
- **Scalability:** Modular Petri net design supports large, complex systems.
- **Model-Based RL Rollouts:** Used to determine optimal AGV positioning, further improving operational efficiency.

This environment (`petrirl-fms-v0`) provides a realistic testbed for dynamic scheduling and resource management in modern manufacturing systems.

## Why PetriRL?

Flexible Manufacturing Systems require adaptive and efficient resource management. PetriRL enhances traditional job shop scheduling by:

- **Integrating AGVs and Tool-Sharing Systems:** Optimizes multiple components simultaneously.
- **Dynamic Action Masking:** Reduces the action space for faster decision-making.
- **Learning-Based Adaptability:** Actor-critic RL adapts to dynamic environments and unexpected events.

## Key Features

- **Colored-Timed Petri Nets (CTPNs):**  
  Model workflows, resource constraints, and timing in FMS. Enable **dynamic action masking**, reducing the action space and improving computational efficiency.

- **Actor-Critic Reinforcement Learning:**  
  Integrates model-based RL with actor-critic methods for adaptive scheduling. Supports lookahead strategies for AGV positioning and tool utilization.

- **Gym-Compatible Environment:**  
  Fully compatible with OpenAI Gym, allowing seamless integration with RL pipelines and rapid experimentation.

- **Benchmarks for Evaluation:**  
  Includes Taillard benchmarks and a new large-scale benchmark inspired by real-world intralogistics scenarios.

- **Enhanced Performance:**  
  Achieves faster computation times while matching or outperforming traditional scheduling methods on makespan metrics.

## Framework Overview

![Framework](https://github.com/Sofiene-Uni/Intralogistics/blob/main/framework.png)

## Installation

Install PetriRL using pip:

```bash
pip install petrirl


## Research Context  

This project builds upon advanced methodologies for FMS optimization:  
- Combines the formalism of Petri Nets with the adaptability of reinforcement learning.  
- Includes a newly developed large-scale benchmark inspired by Taillard instances.  
- Results show improved makespan and computational efficiency, making it suitable for both academic research and industrial applications.  

For more details, refer to the [publication on ResearchGate](https://www.researchgate.net/publication/386198263_Flexible_Manufacturing_Systems_Intralogistics_Dynamic_Optimization_of_AGVs_and_Tool_Sharing_Using_Coloured-Timed_Petri_Nets_and_Actor-Critic_RL_with_Actions_Masking).  

## Contributions  

This project provides:  
- A formalized framework for FMS scheduling.  
- A robust reinforcement learning-based approach for dynamic optimization.  
- Tools for reproducibility, including a Gym-compatible environment and instance generator.  

## Citation  

If you use this framework in your research, please cite the associated papers:  

> **Flexible Manufacturing Systems intralogistics: Dynamic optimization of AGVs and tool sharing using Colored-Timed Petri Nets and actor–critic RL with actions masking**  
> Available from [Link](https://www.sciencedirect.com/science/article/pii/S0278612525001694). 

> **Introducing PetriRL: An innovative framework for JSSP resolution integrating Petri nets and event-based reinforcement learning**  
> Available from [Link](https://www.sciencedirect.com/science/article/pii/S0278612524000943). 

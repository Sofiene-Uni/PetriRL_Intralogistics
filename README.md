
# PetriRL: Advanced Job Shop Scheduling with Petri Nets and Reinforcement Learning  

**PetriRL** is a Python-based framework designed for modeling, simulating, and optimizing job shop scheduling problems using Colored-Timed Petri Nets (CTPNs) and actor-critic reinforcement learning. By combining formal modeling with dynamic action masking and adaptive learning, PetriRL addresses complex challenges in Flexible Manufacturing Systems (FMS), such as automated guided vehicle (AGV) scheduling and tool-sharing optimization.  

## Key Features  

- **Colored-Timed Petri Nets (CTPNs):**  
  PetriRL employs CTPNs to model the intricate dynamics of FMS, providing a formal structure to represent workflows, resource constraints, and timing. CTPNs enable dynamic action masking to reduce the action space, facilitating efficient decision-making.  

- **Actor-Critic Reinforcement Learning:**  
  Integrates model-based reinforcement learning (MBRL) with actor-critic algorithms to adapt policies for dynamic manufacturing environments. PetriRL incorporates lookahead strategies for optimal AGV positioning and tool utilization.  

- **Gym-Compatible Environment:**  
  PetriRL provides an OpenAI Gym-compatible environment, enabling seamless integration with reinforcement learning pipelines and supporting rapid experimentation.  

- **Benchmarks for Evaluation:**  
  Includes support for Taillard Benchmarks and introduces a new large-scale benchmark inspired by real-world scenarios, allowing robust evaluation of scheduling algorithms.  

- **Enhanced Performance:**  
  Demonstrates a tenfold reduction in computation time compared to traditional methods while matching or outperforming them on makespan metrics, especially on large-scale instances.  

## Framework Overview  

![Framework](https://github.com/Sofiene-Uni/Public/raw/main/framework.png)  

## Installation  

Install PetriRL using pip:  

```bash  
pip install petrirl  
```  

## Why PetriRL?  

Flexible Manufacturing Systems (FMS) are critical in modern production due to their ability to adapt to changing demands and optimize resource usage. PetriRL enhances traditional job shop scheduling by:  
1. **Integrating AGVs and Tool-Sharing Systems:** Supports advanced intralogistics with simultaneous optimization of multiple components.  
2. **Dynamic Action Masking:** CTPNs significantly reduce the action space, improving computational efficiency.  
3. **Learning-Based Adaptability:** Actor-critic methods ensure robust policies that adapt to dynamic environments and unforeseen challenges.  

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

> **Introducing PetriRL: An innovative framework for JSSP resolution integrating Petri nets and event-based reinforcement learning**  
> Available from [Link](https://www.sciencedirect.com/science/article/pii/S0278612524000943). 

> **Flexible Manufacturing Systems Intralogistics: Dynamic Optimization of AGVs and Tool Sharing Using Coloured-Timed Petri Nets and Actor-Critic RL with Actions Masking**  
> Available from [Link](https://www.researchgate.net/publication/386198263). 

 

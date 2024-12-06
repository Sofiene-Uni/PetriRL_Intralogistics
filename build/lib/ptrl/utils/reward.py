import numpy as np

def reward(env, feed_back=None, terminal=False):
    """
    Calculate the reward.
    Parameters:
        terminal: if the episode reached termination.
    Returns:
        Any: Calculated reward.
    """
    
    # Pre-fetch relevant places to reduce repeated access
    all_places = env.sim.places.values()
    
    def utilization_reward(role, max_resources):
        # Directly calculate idle resources in one go
        idle_resources = sum(
            1 for p in all_places 
            if p.uid in env.sim.filter_nodes(role) and p.token_container
        )
        return - (idle_resources / max_resources)

    def balance_reward(role):
        places = [p for p in all_places if p.uid in env.sim.filter_nodes(role)]
        processed_tokens = np.array([len(p.history) for p in places])
        
        if processed_tokens.size == 0: 
            return 0
            
        std_dev = np.std(processed_tokens) 
        return -std_dev

    def progress_reward():
        # Calculate finished operations in one loop
        finished_ops = sum(
            len(delivery.token_container) 
            for delivery in all_places 
            if delivery.uid in env.sim.filter_nodes("delivery")
        )
        return finished_ops / (env.sim.clock + 1)
    
    
    def buffer_reward():
        buffer_uids= env.sim.filter_nodes("agv_buffer") + env.sim.filter_nodes("tt_buffer")
        empty_buffers = [p for p in all_places if p.uid in  buffer_uids and not p.token_container]
        return - len(empty_buffers)/len(buffer_uids)

        
    def combined_reward():
       return  0.1* buffer_reward() + 0.9 * utilization_reward("machine_idle", env.sim.n_machines) 
       

    def general_reward():
        if terminal:  
            env.min_makespan = min(env.min_makespan, env.sim.clock)
            return -env.sim.clock
        return 0

    # Reward function dispatch based on env.reward_f
    reward_functions = {
        "M": lambda: utilization_reward("machine_idle", env.sim.n_machines),
        "A": lambda: utilization_reward("agv_idle", env.sim.n_agv),
        "B": lambda: balance_reward("agv_transporting"),
        "T": lambda: utilization_reward("tool_idle", env.sim.n_tt),
        "P": progress_reward,
        "G": general_reward,
        "C" :  combined_reward
    }

    # Call the appropriate reward function or return 0 if not found
    return reward_functions.get(env.reward_f, lambda: 0)()

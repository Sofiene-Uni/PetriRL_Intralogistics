import numpy as np

def get_obs(sim,observation_depth):
    sim_places = sim.places.values()
    observation = []

    for place in sim_places:
        if place.token_container:
            token = place.token_container[0]
            
            try :
                elapsed = token.logging[place.uid][2]
            except: 
                elapsed = 0
            
            observation.extend([
                len(place.token_container),        # x1
                token.rank,                        # x1
                int(token.last_op),                # x1
                *token.color,                      # x3
                *token.machine_sequence,           # x3
                *token.time_features ,             # x5
                token.time_features[1] - elapsed   # x1
            ])
        else:
            observation.extend([0] * 15)  

    return np.array(observation, dtype=np.int64)
 
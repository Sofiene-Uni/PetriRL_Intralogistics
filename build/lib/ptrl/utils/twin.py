import copy


class create_twin():
    
    def __init__(self,sim):
 
        self.policy = None
        self.twin = copy.deepcopy(sim)
        self.max_steps=sim.n_jobs *3  # atleast fire all jobs twince
        

    def sync_state(self, sim):

       self.twin.clock = sim.clock
       
       for place_uid, sim_place in sim.places.items():
           twin_place = self.twin.places.get(place_uid)
           if not twin_place:
               continue
           twin_place.token_container = [copy.deepcopy(token) for token in sim_place.token_container]


    def twin_fire_timed(self, twin):
        """Fire timed transitions based on token timing."""
        role_dict = {
            "machine_processing": 0,
            "agv_transporting": 1,
            "agv_relocating": 2,
            "tt_transporting": 3,
            "tt_relocating": 4,
        }

        for place in (p for p in twin.places.values() if p.type == "p" and p.token_container):
           
            transition = place.children[0]  
            token = place.token_container[0] 
            elapsed_time = token.logging[place.uid][2]
            reference_time = token.time_features[role_dict[place.role]]

            if elapsed_time >= reference_time:
                transition.fire(twin.clock)
                
        twin.refresh_state()  

    def run_lookahead(self, buffer):
        """Run a lookahead simulation to evaluate potential actions."""
       
        twin_buffer = [p for p in self.twin.places.values() if p.uid == buffer.uid][0].token_container
        
        step = 0
        next_position = twin_buffer[0].color[2]  if twin_buffer else None
    

        if self.policy:
            while  not twin_buffer and step < self.max_steps:
                

                obs = self.twin.get_state() 
                mask = self.twin.guard_function() 
                action, _ = self.policy.predict(obs, action_masks=mask) 
                self.twin.fire_controlled(action) 
                
                if twin_buffer:
                    next_position = twin_buffer[0].color[2]
                    return next_position

             
                while sum(self.twin.guard_function()) == 0:
                    self.twin.time_tick() 
                    self.twin_fire_timed(self.twin) 
                    self.twin_fire_timed(self.twin)  
                    
                    if self.twin.is_terminal():  
                        break
                
                step += 1 
             
        # if  next_position  is None  : 
        #     self.twin.graph.plot_net()


if __name__ == "__main__":
    twin = create_twin() 

    
    

import numpy as np
from gymnasium import Env
from gymnasium import spaces

from ptrl.envs.fms.simulator import Simulator
from ptrl.render.plot_fms import JSSPPlotter
from ptrl.utils.reward   import reward


class FmsEnv(Env):
    
    """
    Custom Gym environment for Job Shop Scheduling using a Petri net simulator.
    """
    metadata = {"render_modes": ["solution" , "human"]}

    def __init__(self, 
                 
                 benchmark :str="Raj",
                 instance_id :str="ra01" ,
                 layout:int =1,
                 n_agv:int =1,
                 n_tt:int =0, 
                 
                 dynamic: bool=False,
                 size=(None,None,None,None),
                 
                 observation_depth:int = 1 , 
                 reward_f:str="",
                 render_mode: str ="solution",
                 lookup: bool= False,
                 
                 grid=False,
                 rank= False,
                 
                 
                 ):
        """
        Initializes the JsspetriEnv.
        if the JSSP is flexible a maximum number of machines and jobs if predefined regardless le instance size 

        Parameters:
            render_mode (str): Rendering mode ("human" or "solution").
            instance_id (str): Identifier for the JSSP instance.
            observation_depth (int): Depth of observations in future.
        """
        
        self.dynamic=dynamic
        self.instance_id=instance_id
        
        self.sim = Simulator(
                             benchmark=benchmark,
                             instance_id=self.instance_id,
                             layout=layout,
                             n_agv=n_agv,
                             n_tt=n_tt,
                             
                             dynamic=self.dynamic,
                             size=size,

                             observation_depth=observation_depth,
                             lookup=lookup
                             )


        observation_size = 15 *len(self.sim.places.values()) 
            
        self.observation_space= spaces.Box(low=-1, high=self.sim.max_bound,shape=(observation_size,),dtype=np.int64)
        self.action_space = spaces.Discrete(len(self.sim.action_map))  
      
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.reward_f=reward_f
        
        self.plotter=JSSPPlotter(grid=grid, rank=rank, title_font_size=24, font_size=20,  format="pdf", dpi=300)
        
        self.min_makespan=np.inf
        print(f"Reward function: {reward_f} , Render_mode: {render_mode}")

 

    def reset(self, seed=None, options=None):
        """
        Reset the environment.
        Returns:
            tuple: Initial observation and info.
        """
        self.sim.petri_reset()
        observation=self.sim.get_state()
        info = self._get_info(0,False,False)
        return observation, info
    
    
    def reward(self,feed_back=None,terminal=False):
       """
       Calculate the reward.
       Parameters:
           terminal: if the episode reached termination.
       Returns:
           Any: Calculated reward .
       """ 
       return reward(self,feed_back,terminal)


    def action_masks(self):
        """
        Get the action masks.
        Returns:
            list: List of enabled actions.
        """ 
        return self.sim.guard_function()
    
    def step(self, action):
        """
        Take a step in the environment.
        Parameters:
            action: Action to be performed.
        Returns:
            tuple: New observation, reward, termination status, info.
            
        """
        
        screenshot= True if self.render_mode == "human" else False
        
        feedback = self.sim.interact(action,screenshot=screenshot)  
        observation = self.sim.get_state()
        terminated= self.sim.is_terminal()
        reward = self.reward(feedback,terminated)
        info = self._get_info()
        return observation, reward, terminated, False, info
    

    def render(self):
        """
        Render the environment.
        """
        if self.render_mode ==  "solution":
            self.plotter.plot_solution(self.sim)

        if self.render_mode == "human":
            self.plotter.plot_solution(self.sim)
            # lunch GUI to display imag sequence , TO DO 
 

    def close(self):
        """
        Close the environment.
        """

    def _get_info(self, reward=0,fired=False, terminated=False):
        """
        Get information dictionary.
        """
        return {"Reward": reward,"Fired":fired ,"Terminated": terminated ,"mask":self.sim.guard_function()}

if __name__ == "__main__":
    
    instance="ra01"
    agvs=2
    tools_transport=1
    
    dynamic=False
    
    # Job,machines,n_agvs,n_tools,ntt
    size=(100,20,10,0,0)
    
    env=FmsEnv(instance_id=instance,dynamic=dynamic,size=size,n_agv=agvs ,n_tt=tools_transport)
    
    observation,info=env.reset()
    


    

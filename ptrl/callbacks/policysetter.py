from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import VecEnv


class PolicyCallback(BaseCallback):
    def __init__(self, env, verbose=0):
        super(PolicyCallback, self).__init__(verbose)
        self.env = env

    def _on_rollout_start(self):
        
        # Handle vectorised multi-environment case
        if isinstance(self.env, VecEnv):

            original_envs = self.env.get_attr('sim')  
            for original_env in original_envs:
                if original_env.lookup:
                    original_env.twin.policy = self.model.policy
                    if self.verbose > 0:
                        print("Policy has been set in the environment at the start of the episode.")
                else:
                    if self.verbose > 0:
                        print("Sim lookup failed or is not available.")
        else:
            # Handle single environment case
            original_env = self.env.sim
            if original_env.lookup:
                original_env.twin.policy = self.model.policy
                if self.verbose > 0:
                    print("Policy has been set in the environment at the start of the episode.")
            else:
                if self.verbose > 0:
                    print("Sim lookup failed or is not available.")

    def _on_step(self):
        return True  # Continue training
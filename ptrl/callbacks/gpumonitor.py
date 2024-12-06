import GPUtil
from stable_baselines3.common.callbacks import BaseCallback

class GpuCallback(BaseCallback):
    def __init__(self, env, check_freq=1000, verbose=0):
        """
        :param env: The environment to monitor.
        :param check_freq: How often (in steps) to log GPU usage.
        :param verbose: Verbosity level (0 or 1).
        """
        super(GpuCallback, self).__init__(verbose)
        self.env = env
        self.check_freq = check_freq

    def _on_step(self):
        if self.num_timesteps % self.check_freq == 0:
            self.log_gpu_usage()

        return True  

    def log_gpu_usage(self):
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print(f"Step {self.num_timesteps}:")
            print(f"  GPU ID: {gpu.id}")
            print(f"  GPU Name: {gpu.name}")
            print(f"  GPU Load: {gpu.load * 100:.2f}%")
            print(f"  GPU Memory Free: {gpu.memoryFree} MB")
            print(f"  GPU Memory Used: {gpu.memoryUsed} MB")
            print(f"  GPU Memory Total: {gpu.memoryTotal} MB")
            print(f"  GPU Temperature: {gpu.temperature} °C")
            print("-" * 30)


import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from distutils.spawn import find_executable

class JSSPPlotter:
 
    def __init__(self, grid=True, rank=True, title_font_size=18, font_size=16,  format="png", dpi=150):
        self.grid = grid
        self.rank = rank
        self.title_font_size = title_font_size
        self.font_size = font_size
        self.format = format
        self.dpi = dpi
   
        if find_executable('latex'):
            plt.rc('text', usetex=True)
        else:
            plt.rc('text', usetex=False)
                    
    def create_directory(self, directory_path):
        """Create a directory if it does not exist."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def get_file_path(self, jssp):
        """Generate the file path for saving the plot."""
        renders_folder = os.path.join(os.getcwd(), "renders")
        self.create_directory(renders_folder)

        solution_folder = os.path.join(renders_folder, str(jssp.instance_id))
        self.create_directory(solution_folder)

        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return os.path.join(solution_folder, f"{current_datetime}.{self.format}")

    def plot_solution(self, jssp):
        """Plot the JSSP solution based on the number of AGVs and transport tasks."""
        file_path = self.get_file_path(jssp)

        if jssp.n_agv > 0 and jssp.n_tt > 0:
            fig = self.solution_agv_tt(jssp)
        elif jssp.n_agv > 0:
            fig = self.solution_agv(jssp)
        else:
            fig = self.solution_basic(jssp)

        plt.tight_layout()
        plt.show()
        fig.savefig(file_path, format=self.format, dpi=self.dpi)

    def setup_plot(self, ax, title, xlabel):
        """Set up the axes with titles and labels."""
        
        ax.tick_params(axis='x', labelsize=self.font_size)
        ax.tick_params(axis='y', labelsize=self.font_size)
        
        # Adding padding below the title and above the x-axis label
        ax.set_title(title, fontsize=self.title_font_size, fontweight='bold', pad=10) 
        ax.set_xlabel(xlabel, fontsize=self.title_font_size, labelpad=15)  


    def draw_bars(self, ax, data_df, y_col, left_col, width_col, color_col):
        """Draw horizontal bars on the provided axes."""
        bars = ax.barh(
            y=data_df[y_col],
            left=data_df[left_col],
            width=data_df[width_col],
            height=0.5,
            color=data_df[color_col]
        )
        return bars

    def annotate_plot(self, jssp, ax, data_df, bars, deadheading=False):
        """Annotate bars with ranks or other information."""
        if self.rank and deadheading:
            for bar, source, destination in zip(bars, data_df["from_location"], data_df["to_location"]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                         f'{source}', ha='center', va='bottom', color='black', fontsize=self.font_size)
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                         f'{destination}', ha='center', va='top', color='black', fontsize=self.font_size)
        elif self.rank:
            for bar, rank in zip(bars, data_df["token_rank"]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                         f'{rank}', ha='center', va='center', color='black', fontsize=self.font_size)

        if self.grid:
            step = 1
            for step in range(0, jssp.clock, step):
                ax.axvline(x=step, color='grey', linestyle='--', linewidth=0.5, alpha=0.3)

    def create_legend(self, ax, jobs_df, color_map, title):

        
        unique_jobs = sorted(jobs_df['jobs'].unique())
        cmap = plt.cm.get_cmap("tab20b", len(unique_jobs))
        color_mapping = {job_number: cmap(i) for i, job_number in enumerate(unique_jobs)}
    
        # Create legend patches
        legend_patches = [plt.Line2D([0], [0], color='gray', lw=5, label='Deadheadings')]
        legend_patches.extend([plt.Line2D([0], [0], color=color, lw=5, label=str(job_number))
                               for job_number, color in color_mapping.items()])
    
        # Adjust bbox_to_anchor to add space before the legend
        legend = ax.legend(
            handles=legend_patches,
            title=title,
            title_fontsize=self.title_font_size,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.35),  # Increase negative y-value for more space
            ncol=10,
            handlelength=1
        )
    
        # Customize text font size in legend
        for text in legend.get_texts():
            text.set_fontsize(self.font_size)


    def get_color_mapping(self, jssp):
        job_df = self.create_job_data(jssp)
        unique_jobs = sorted(set(job_df["jobs"]))
        cmap = plt.cm.get_cmap("tab20b", len(unique_jobs))
        return {job_number: cmap(i) for i, job_number in enumerate(unique_jobs)}

    def create_job_data(self, jssp):
        """Extract job-related data into a dictionary."""
        jssp_data_dict = {
            "machine_id": [],
            "token_rank": [],
            "entry_values": [],
            "process_times": [],
            "jobs": []
        }
        finished_tokens = jssp.delivery_history[list(jssp.delivery_history.keys())[-1]]

        for token in finished_tokens:
            for uid, entry in token.logging.items():
                if uid in jssp.filter_nodes("machine_processing"):
                    jssp_data_dict["machine_id"].append(f"M {str(jssp.places[uid].color).zfill(2)}")
                    jssp_data_dict["jobs"].append(token.color[0])
                    jssp_data_dict["token_rank"].append(token.rank)
                    jssp_data_dict["entry_values"].append(entry[0])
                    jssp_data_dict["process_times"].append(entry[2])

        return pd.DataFrame(jssp_data_dict).sort_values('machine_id')

    def create_agv_data(self, jssp):
        """Extract AGV-related data into a dictionary."""
        agv_data_dict = {
            "agv_id": [],
            "token_rank": [],
            "entry_values": [],
            "process_times": [],
            "token_role": [],
            "jobs": []
        }

        finished_tokens = jssp.delivery_history[list(jssp.delivery_history.keys())[-1]]
        for token in finished_tokens:
            for uid, entry in token.logging.items():
                if uid in jssp.filter_nodes("agv_transporting"):
                    agv_data_dict["agv_id"].append(f"AGV {str(jssp.places[uid].color).zfill(2)}")
                    agv_data_dict["jobs"].append(token.color[0])
                    agv_data_dict["token_rank"].append(token.rank)
                    agv_data_dict["token_role"].append(token.role)
                    agv_data_dict["entry_values"].append(entry[0])
                    agv_data_dict["process_times"].append(entry[2])

        return pd.DataFrame(agv_data_dict).sort_values('agv_id')
    
    
    
    def create_agv_deadheading_data(self,jssp):
        """Extract AGV deadheading-related data into a dictionary."""
        agv_deadheading_dict = {
            "agv_id": [],
            "from_location": [],
            "to_location": [],
            "entry_values": [],
            "process_times": [],
        }
    
        finished_tokens = jssp.delivery_history[list(jssp.delivery_history.keys())[-1]]
    
        for token in finished_tokens:
            if token.deadheadings['agv_transporting']:
                agv_deadheading_dict["agv_id"].append(f"AGV {str(token.deadheadings['agv_transporting'][0][0]).zfill(2)}")
                agv_deadheading_dict["from_location"].append(token.deadheadings['agv_transporting'][0][1])
                agv_deadheading_dict["to_location"].append(token.deadheadings['agv_transporting'][0][2])
                agv_deadheading_dict["entry_values"].append(token.deadheadings['agv_transporting'][0][3])
                agv_deadheading_dict["process_times"].append(token.deadheadings['agv_transporting'][0][4])
    
        return pd.DataFrame(agv_deadheading_dict).sort_values('agv_id')
    
    
    def create_tt_data(self,jssp):
        """Extract TT-related data into a dictionary."""
        tt_data_dict = {
            "tt_id": [],
            "token_rank": [],
            "entry_values": [],
            "process_times": [],
            "token_role": [],
            "jobs": []
        }
    
        finished_tokens = jssp.delivery_history[list(jssp.delivery_history.keys())[-1]]
    
        for token in finished_tokens:
            for uid, entry in token.logging.items():
                if uid in jssp.filter_nodes("tt_transporting"):
                    tt_data_dict["tt_id"].append(f"TT {str(jssp.places[uid].color).zfill(2)}")
                    tt_data_dict["jobs"].append(token.color[0])
                    tt_data_dict["token_rank"].append(token.rank)
                    tt_data_dict["token_role"].append(token.role)
                    tt_data_dict["entry_values"].append(entry[0])
                    tt_data_dict["process_times"].append(entry[2])
                    
        return pd.DataFrame(tt_data_dict).sort_values('tt_id')
    
    
    
    
    def create_tt_deadheading_data(self,jssp):
        """Extract TT deadheading-related data into a dictionary."""
        tt_deadheading_dict = {
            "tt_id": [],
            "from_location": [],
            "to_location": [],
            "entry_values": [],
            "process_times": [],
        }
    
        finished_tokens = jssp.delivery_history[list(jssp.delivery_history.keys())[-1]]
    
        for token in finished_tokens:
            if token.deadheadings["tt_transporting"]:
                tt_deadheading_dict["tt_id"].append(f"TT {str(token.deadheadings['tt_transporting'][0][0]).zfill(2)}")
                tt_deadheading_dict["from_location"].append(token.deadheadings['tt_transporting'][0][1])
                tt_deadheading_dict["to_location"].append(token.deadheadings['tt_transporting'][0][2])
                tt_deadheading_dict["entry_values"].append(token.deadheadings['tt_transporting'][0][3])
                tt_deadheading_dict["process_times"].append(token.deadheadings['tt_transporting'][0][4])
    
        return pd.DataFrame(tt_deadheading_dict).sort_values('tt_id')
    
    

    def solution_basic(self, jssp):
        """Plot the basic solution without AGVs."""
        fig, ax = plt.subplots(figsize=(15, 10))
        jobs_df = self.create_job_data(jssp)
        color_mapping = self.get_color_mapping(jssp)
        jobs_df['color'] = jobs_df['jobs'].map(color_mapping)

        self.setup_plot(ax, f"Machines Schedule for instance {jssp.instance_id}", f"Makespan: {jssp.clock} steps")
        bars = self.draw_bars(ax, jobs_df, "machine_id", "entry_values", "process_times", "color")
        self.create_legend(ax, jobs_df, color_mapping, "Job_id")
        self.annotate_plot(jssp, ax, jobs_df, bars)
        return fig


    def solution_agv(self, jssp , gridresize = False):
        """Plot the solution including AGVs."""
          
        gridspec_kw=None
        if gridresize:
            total = jssp.n_machines + jssp.n_agv + jssp.n_tt
            gridspec_kw={'height_ratios': [jssp.n_machines/total, jssp.n_agv/total,jssp.n_tt/total]}
        
        fig, axes = plt.subplots(2,1, figsize=(15, 10), sharex=True, gridspec_kw=gridspec_kw)  
        ax1, ax2 = axes
        
        jobs_df = self.create_job_data(jssp)
        agv_df = self.create_agv_data(jssp)
        agv_deadheading_df = self.create_agv_deadheading_data(jssp)
        color_mapping = self.get_color_mapping(jssp)
    
        jobs_df['color'] = jobs_df['jobs'].map(color_mapping)
        agv_df['color'] = agv_df['jobs'].map(color_mapping)
        agv_deadheading_df['color'] = 'grey'
    
        job_bars = self.draw_bars(ax1, jobs_df, "machine_id", "entry_values", "process_times", "color")
        agv_bars = self.draw_bars(ax2, agv_df, "agv_id", "entry_values", "process_times", "color")
        agv_deadheading_bars = self.draw_bars(ax2, agv_deadheading_df, "agv_id", "entry_values", "process_times", "color")
    
        self.setup_plot(ax1, f"Machines Schedule for instance {jssp.instance_id}", "")
        self.setup_plot(ax2, f"AGVs Schedule for instance {jssp.instance_id}", f"Makespan: {jssp.clock} steps")
        
        self.annotate_plot(jssp, ax1, jobs_df, job_bars) 
        self.annotate_plot(jssp, ax2, agv_df, agv_bars)
        self.annotate_plot(jssp, ax2, agv_deadheading_df, agv_deadheading_bars, deadheading=True)
    
        self.create_legend(ax2, jobs_df, color_mapping, "Job_id")
        
        return fig

    def solution_agv_tt(self, jssp ,gridresize=False):
        """Plot the solution including AGVs and tool transports with dynamic subplot sizes."""
  
        # Define proportional heights for the subplots based on the number of bars
        
        gridspec_kw=None
        if gridresize:
            total = jssp.n_machines + jssp.n_agv + jssp.n_tt
            gridspec_kw={'height_ratios': [jssp.n_machines/total, jssp.n_agv/total,jssp.n_tt/total]}
        
        fig, axes = plt.subplots(3,1, figsize=(15, 15), sharex=True, gridspec_kw=gridspec_kw)
        
        ax1, ax2, ax3 = axes
        
        # Prepare data
        jobs_df = self.create_job_data(jssp)
        agv_df = self.create_agv_data(jssp)
        tt_df = self.create_tt_data(jssp)
        agv_deadheading_df = self.create_agv_deadheading_data(jssp)
        tt_deadheading_df = self.create_tt_deadheading_data(jssp)
        color_mapping = self.get_color_mapping(jssp)
        
        # Map colors
        jobs_df['color'] = jobs_df['jobs'].map(color_mapping)
        agv_df['color'] = agv_df['jobs'].map(color_mapping)
        tt_df['color'] = tt_df['jobs'].map(color_mapping)
        agv_deadheading_df['color'] = 'grey'
        tt_deadheading_df['color'] = 'grey'
        
        # Draw bars
        job_bars = self.draw_bars(ax1, jobs_df, "machine_id", "entry_values", "process_times", "color")
        agv_bars = self.draw_bars(ax2, agv_df, "agv_id", "entry_values", "process_times", "color")
        agv_deadheading_bars = self.draw_bars(ax2, agv_deadheading_df, "agv_id", "entry_values", "process_times", "color")
        tt_bars = self.draw_bars(ax3, tt_df, "tt_id", "entry_values", "process_times", "color")
        tt_deadheading_bars = self.draw_bars(ax3, tt_deadheading_df, "tt_id", "entry_values", "process_times", "color")
        
        # Setup plots
        self.setup_plot(ax1, f"Machines Schedule for instance {jssp.instance_id}", "")
        self.setup_plot(ax2, "AGVs Schedule", "")
        self.setup_plot(ax3, "Tools Transport Schedule", f"Makespan: {jssp.clock} steps")
        
        # Annotate plots
        self.annotate_plot(jssp, ax1, jobs_df, job_bars)
        self.annotate_plot(jssp, ax2, agv_df, agv_bars)
        self.annotate_plot(jssp, ax3, tt_df, tt_bars)
        self.annotate_plot(jssp, ax2, agv_deadheading_df, agv_deadheading_bars, deadheading=True)
        self.annotate_plot(jssp, ax3, tt_deadheading_df, tt_deadheading_bars, deadheading=True)
        
        # Create legend
        self.create_legend(ax3, jobs_df, color_mapping, "Job_id")
        
        return fig
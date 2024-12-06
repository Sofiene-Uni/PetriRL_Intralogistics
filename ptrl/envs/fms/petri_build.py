import copy 
from ptrl.common.instance_loader import InstanceLoader
from ptrl.common.build_blocks import  IdGen,Token, Place, Transition

class Petri_build:
    """
    A class representing a Petri net for Job Shop Scheduling Problems (JSSP).

    Attributes:
        instance_id (str): The ID of the JSSP instance.
        instance (pd.DataFrame): The JSSP instance data.
        n_jobs (int): The number of jobs in the instance.
        n_machines (int): The number of machines in the instance.
        max_bound (int): The maximum number of operations or tokens.

        places (dict): A dictionary containing Place objects.
        transitions (dict): A dictionary containing Transition objects.
    """

    def __init__(self, instance_id,
                 
                 layout=1,
                 benchmark='Raj',
                 n_agv=1,
                 n_tt=0,
                 dynamic=False,
                 size=(100,20,10,0,0)   #jobs , machines , agvs , tools , tool transport 
                 ):
        """
        Initialize the Petri net with a JSSP instance.

        Parameters:
            instance_id (str): The ID of the JSSP instance.
            dynamic (bool): If True, the Petri net is dynamic.
            size (tuple): Size parameters for dynamic mode (default: (100, 20)).
            n_agv (int): Number of AGVs (default: 0).
            n_tt (int): Number of tool transports (default: 0).
            benchmark (str): Benchmark type for instance loading (default: 'Raj').
        """
        
        self.layout=layout
        self.benchmark=benchmark
        
        
        self.instance_id = instance_id
        self.instance=InstanceLoader(benchmark=benchmark,instance_id=instance_id,layout=layout) 
        self.n_jobs, self.n_machines, self.n_tools, self.max_bound = self.instance.specs
         
        self.n_agv = n_agv
        self.n_tt = n_tt
        
        self.places = {}
        self.transitions = {}
        
        self.dynamic = dynamic
        if self.dynamic:
            self.n_jobs, self.n_machines,self.n_agv,self.n_tools,self.n_tt = size
            
        
        self.number_of_ops=0
            
       

    def __str__(self):
        """
        Get a string representation of the Petri net.

        Returns:
            str: A string representing the Petri net.
        """
        return f"JSSP {self.instance_id}: {self.n_jobs} jobs X {self.n_machines} machines"

    def filter_nodes(self, node_role):
        """
        Filters nodes based on node role.

        Parameters:
            node_role (str): Role of nodes to filter.

        Returns:
            list: Filtered nodes.
        """
        filtered_nodes = []
        for place in self.places.values():
            if place.role in node_role:
                filtered_nodes.append(place.uid)

        for transition in self.transitions.values():
            if transition.role == node_role:
                filtered_nodes.append(transition.uid)
        return filtered_nodes

    def node_info(self, node_uid, display=False):
        """
        Retrieves information about a node based on its UID.

        Parameters:
            node_uid (str): UID of the node.
            display (bool): If True, print node information (default: False).

        Returns:
            object: The node object corresponding to the UID.
        """
        for node in list(self.places.values()) + list(self.transitions.values()):
            if node.uid == node_uid:
                if display:
                    print(node)
                return node

        print("Node not found!")

    def add_nodes_layer(self, genre="place", type_="", role="", colored=False, timed=False, show=True, number=1):
        """
        Add a layer of nodes (places or transitions) to the Petri net.

        Parameters:
            genre (str): Type of nodes ("place" or "trans").
            type_ (str): Type of the node.
            role (str): Role of the node.
            colored (bool): If True, nodes are colored.
            timed (bool): If True, nodes are timed.
            show (bool): If True, show nodes (default: True).
            number (int): Number of nodes to add.
        """
        if genre == "place":
            for i in range(1,number+1):
                
                color = i if colored else None
                place_name = f"{role} {i}"
                place = Place(label=place_name, type_=type_, role=role, color=color, timed=timed, show=show)
                self.places[place.uid] = place
        else:
            for i in range(1,number+1):  
                color = i if colored else None
                transition_name = f"{role} {i}"
                transition = Transition(label=transition_name, type_=type_, role=role, color=color, timed=timed, show=show)
                self.transitions[transition.uid] = transition

    def add_connection(self, parent_role, child_role, contype="p2t", fc=False):
        """
        Add connections (arcs) between nodes in the Petri net.

        Parameters:
            parent_role (str): Role of parent nodes.
            child_role (str): Role of child nodes.
            contype (str): Connection type ("p2t" for place to transition, "t2p" for transition to place).
            fc (bool): True for a fully connected graph, False for pairwise connections.
        """
        if contype == "p2t":
            parent_nodes = [p for p in self.places.values() if p.role == parent_role]
            child_nodes = [t for t in self.transitions.values() if t.role == child_role]
        
        elif contype == "t2p":
            parent_nodes = [t for t in self.transitions.values() if t.role == parent_role]
            child_nodes = [p for p in self.places.values() if p.role == child_role]

        if fc:
            for parent in parent_nodes:
                for child in child_nodes:
                    parent.add_arc(child, parent=False)
                    child.add_arc(parent, parent=True)
        else:
            for parent, child in zip(parent_nodes, child_nodes):
                parent.add_arc(child, parent=False)
                child.add_arc(parent, parent=True)

    def add_tokens(self):
        """
        Add tokens (representing job operations) to the Petri net.
        """
       
        for place in self.places.values():
            if  place.type=="f"  : 
                place.token_container.append(Token(color=(0,0,0 )))  
                
                
     
        for job, uid in enumerate(self.filter_nodes("job"), start=1):  
            previous_machine = 0
            last_op=False
           
            try : # only add token to the operation in the instance  (for dynamic variant ) 
            
                # operations tokens
                job_sequence = self.instance.job_sequences[job - 1]  
                for i, (machine, tool, process_time) in enumerate(job_sequence, start=1):
                    
                    if i < len(job_sequence):
                        next_machine = job_sequence[i][0] 
                        
                    elif i == len(job_sequence) :
                        last_op=True
                        next_machine = 0 
                        
                    else:
                        next_machine = 0 
                        
                    agv_loaded =self.instance.get_time(previous_machine, machine, time_type=1) 
                    tt_loaded =self.instance.get_time(previous_machine, machine, time_type=2) 
                    
                    
                    # Create and append the token with the previous, current, and next machine in sequence
                    self.places[uid].token_container.append(
                        Token(initial_place=uid,
                              color=(job, machine, tool),
                              
                              # process_time, loaded_transport , avg_deadhead ,tool_transport,, tt_deadhead 
                              time_features=[process_time, agv_loaded, 0, tt_loaded,0 ],  
                              rank=i,
                              machine_sequence=(previous_machine, machine, next_machine),
                              last_op=last_op
                              ))
                    
                    self.number_of_ops+=1
                    previous_machine = machine
                    
                    
            except Exception as e : 
                if self.dynamic :
                    pass # the reserve jobs are empty 
                else :
                    print(f"Error in adding the tokens: {e}")
                    
                

 
    
    def create_petri(self,show_flags=False,show_develop=False):
        """
        Create the Petri net structure with predefined nodes and connections.

        Parameters:
            LU (bool): If True, include load and unload operations.
            show_flags (bool): If True, show flags in node creation.
        """
        
        IdGen.reset()

        #genre="place", type_="", role="", colored=True, timed=False, show=True, number=1 
        nodes_layers = [

            ("place", "s", "job_sorting",  False, False, show_develop, 1), 
            ("trans", "a", "job_sort",  True, False, show_flags, self.n_jobs),
            ("place", "f", "job_idle",  True, False, show_flags, self.n_jobs),
            ("place", "b", "job", True, False, True, self.n_jobs),
            ("trans", "c", "job_select",  False, False, True, self.n_jobs),
            ("place", "s", "machine_sorting",  False, False, True, 1),
            ("trans", "a", "machine_sort",  True, False, True, self.n_machines),
            ("place", "b", "machine_buffer",  True, False, True, self.n_machines,),
            ("trans", "a", "machine_start",  False, False, True, self.n_machines),
            ("place", "p", "machine_processing",  True, True, True, self.n_machines),
            ("place", "f", "machine_idle",  False, False, show_flags, self.n_machines),
            ("trans", "t", "machine_finish",  False, True, True, self.n_machines),
            ("place", "d", "delivery",  False, False, True, self.n_machines),
            
         ]
        
        layers_to_connect = [
            
            ("job_sorting", "job_sort", "p2t", True),
            ("job_sort", "job_idle", "t2p", False),
            ("job_idle", "job_select", "p2t", False),
            ("job", "job_select", "p2t", False),
            ("machine_sorting", "machine_sort", "p2t", True),
            ("machine_sort", "machine_buffer", "t2p", False),
            ("machine_buffer" ,"machine_start","p2t", False),
            ("machine_idle", "machine_start", "p2t", False),
            ("machine_start", "machine_processing", "t2p", False),
            ("machine_processing", "machine_finish", "p2t", False),
            ("machine_finish", "machine_idle", "t2p", False),
            ("machine_finish", "delivery", "t2p", False),
            ("machine_finish", "job_sorting", "t2p", True),
            ("machine_sorting", "lu", "p2t", False),

        ]
        
        if self.n_agv > 0 :
            
            nodes_layers += [
                ("place", "b", "oprations_buffer",  False, False, True, 1),
                ("trans", "c", "agv_select",  True, False, True,self.n_agv),
                ("place", "b", "agv_buffer",  True, False, True, self.n_agv),
                ("trans", "a", "agv_start",  True, False, True, self.n_agv),
                ("place", "p", "agv_transporting", True, True, True, self.n_agv),
                ("trans", "t", "agv_finish",  True, True, True, self.n_agv),
                ("place", "b", "agv_idle",  True, True, show_flags, self.n_agv),
                ("transition", "a", "agv_relocate",  True, True, show_flags, self.n_agv),
                ("place", "p", "agv_relocating",  True, True, show_flags, self.n_agv),
                ("transition", "t", "agv_relocated",  True, True, show_flags, self.n_agv),
                ("place", "f", "agv_ready",  True, True, show_flags, self.n_agv),
                
            ]
            layers_to_connect += [
                ("job_select", "oprations_buffer", "t2p", True),
                ("oprations_buffer", "agv_select", "p2t", True),
                ("agv_select", "agv_buffer", "t2p", False),
                ("agv_buffer", "agv_start", "p2t", False),
                ("agv_start", "agv_transporting", "t2p", False),
                ("agv_transporting", "agv_finish", "p2t", False),
                ("agv_finish", "machine_sorting", "t2p", True),
                ("agv_finish","agv_idle", "t2p", False),
                ("agv_idle","agv_relocate", "p2t", False),
                ("agv_relocate","agv_relocating", "t2p", False),
                ("agv_relocating","agv_relocated", "p2t", False),
                ("agv_relocated","agv_ready", "t2p", False),
                ("agv_ready","agv_start", "p2t", False),
                 
                ]
        else :
            layers_to_connect += [("job_select", "machine_sorting", "t2p", True)]
                
        if self.n_tt > 0 :
            nodes_layers += [
                
                ("place", "s", "request_sorting",  False, False, True, 1),
                ("trans", "a", "request_sort",  True, False, True, self.n_tools),
                ("place", "b", "tool_requests",  True, False, True, self.n_tools),
                ("place", "f", "tool_idle",  True, False, show_flags, self.n_tools),
                ("trans", "c", "tool_select",  False, False, True, self.n_tools),             
                ("place", "f", "tool_transport_idle",  False, False, show_flags, self.n_tt),
                ("place", "b", "tool_requests_buffer",  True, False, True, 1),
                
                
                ("trans", "c", "tt_select",  False, False, True, self.n_tt),  
                ("place", "b", "tt_buffer",  False, False, True, self.n_tt),  
                ("trans", "a", "tt_start",  False, False, True, self.n_tt),     
                ("place", "p", "tt_transporting",  True, True, True, self.n_tt),
                ("trans", "t", "tt_finish",  False, True, True, self.n_tt),
                ("place", "b", "tt_idle",  True, True, show_flags, self.n_tt),
                ("transition", "a", "tt_relocate",  True, True, show_flags, self.n_tt),
                ("place", "p", "tt_relocating",  True, True, show_flags, self.n_tt),
                ("transition", "t", "tt_relocated",  True, True, show_flags, self.n_tt),
                ("place", "f", "tt_ready",  True, True, show_flags, self.n_tt),
  
    
                ("place", "s", "machine_sorting_T",  False, False, True, 1),
                ("trans", "a", "machine_sort_T",  True, False, True, self.n_machines),
                ("place", "b", "machine_buffer_T",  True, False, True, self.n_machines),
                ("place", "s", "tools_sorting",  False, False, show_develop, 1),  
                ("trans", "a", "tool_sort",  True, False, show_flags, self.n_tools)
                ]
            layers_to_connect += [ 
                
                ("job_select", "request_sorting", "t2p", True),
                ("request_sorting", "request_sort", "p2t", True),
                ("request_sort", "tool_requests", "t2p", False),
                ("tool_requests", "tool_select", "p2t", False),
                ("tool_idle", "tool_select", "p2t", False),
                ("tool_select", "tool_requests_buffer","t2p", True),
                ("tool_requests_buffer","tt_select","p2t", True),
                
                ("tt_select","tt_buffer","t2p", False),
                ("tt_buffer","tt_start","p2t", False),
                ("tt_ready","tt_start", "p2t", False),
                ("tt_start",  "tt_transporting", "t2p", False),
                ("tt_transporting", "tt_finish" , "p2t", False),
                ("tt_finish", "tt_idle", "t2p", False),
                ("tt_idle","tt_relocate", "p2t", False),
                ("tt_relocate","tt_relocating", "t2p", False),
                ("tt_relocating","tt_relocated", "p2t", False),
                ("tt_relocated","tt_ready", "t2p", False),
             
                ("tt_finish", "machine_sorting_T", "t2p", True),
                ("machine_sorting_T", "machine_sort_T", "p2t", True),
                ("machine_sort_T", "machine_buffer_T", "t2p", False),
                ("machine_buffer_T", "machine_start", "p2t", False),
                ("machine_finish", "tools_sorting", "t2p", True),
                ("tools_sorting", "tool_sort", "p2t", True),
                ("tool_sort", "tool_idle", "t2p", False), 
                ]
            
        for genre,type_, role, colored, timed, show, number in nodes_layers:
            self.add_nodes_layer(genre=genre, type_=type_, role=role, colored=colored, timed=timed, show=show, number=number)

        for parent_role, child_role, contype, full_connect in layers_to_connect:
            self.add_connection(parent_role, child_role, contype, full_connect)
            
        
            

# %% Test
if __name__ == "__main__":
    
    benchmark='Raj'
    instance_id= "ra01"
    layout =1
    n_agv= 2
    n_tt= 0
    
    dynamic=False
    
    # Job,machines,n_agvs,n_tools,ntt
    size=(100,20,10,0,0)
    
    petri=Petri_build(instance_id,layout, benchmark=benchmark ,n_agv=n_agv , n_tt=n_tt,dynamic=dynamic,size=size) 
    petri.create_petri()    
    petri.add_tokens()
    
    
    
    
    jobs = [p for p in petri.places.values() if p.uid in petri.filter_nodes("job")]

    for job in jobs :
        print(len(job.token_container))
        for token  in job.token_container:
            print(token)
            
            
    
    # benchmark="Raj"
    # instance_id= "ra01"
    # layout=1
    # layout =1
    # n_agv= 1
    # n_tt= 0
    
    # dynamic=False
    # # Job,machines,n_agvs,n_tools,ntt
    # size=(100,20,10,0,0)
    
    # petri=Petri_build(instance_id,layout, benchmark=benchmark ,n_agv=n_agv , n_tt=n_tt,dynamic=dynamic,size=size)
    
    
    
   
        

    
    
    

    
    


    
    




    
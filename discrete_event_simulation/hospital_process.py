import numpy as np

class HospitalProcess:
    '''
    Defines the default structure for a process within the simulation.
    The emergency department processes typically share the following common attributes:
    1. random.uniform distribution for timing
    2. list of resource(s) allocated to process
    3. unique name allocated to process

    Thus, to simplify the implementation, I defined a single class that encapsulates these features.

    The class consists of the following functions:
    
    1. __init__(env, task_name, resource_names, time_range, shared_resources):
        a. Used to initialise specific variables during class instantiation as an object.
    
    2. run()
        a. Used to run the entire process timeline (from resource allocation, to wait for process completion).


    3. request_resource_and_monitor_time(resource_to_request, request_process)
        a. Used to offload resource requesting and wait time monitoring, to parallelise the resource request
        queue for processes with multiple resource requirements.
    

    The class has the following attributes:
          1. env: The SimPy environment.
          2. task_name: A string to name the task.
          3. resource_names: A list of strings representing keys in the shared resource pool.
          4. time_min : Minimum service duration to select from the random distribution
          5. time_max : Maximum service duration to select from the random distribution.
          6. shared_resources: The shared resource pool (a dictionary of SimPy resources).
          7. resource_wait_times : The wait times recorded for each resource in the process.
    '''
    def __init__(self, env, task_name, resource_names, time_range, shared_resources):
        self.env = env
        self.task_name = task_name
        self.resource_names = resource_names
        self.time_min = time_range[0]
        self.time_max = time_range[1]
        self.shared_resources = shared_resources

    def run(self):
        self.resource_wait_times = {}
        request_store = [self.shared_resources[res].request() for res in self.resource_names]
        parallel_requests = [self.env.process(self.request_resource_and_monitor_time(res, req))
                             for res, req in zip(self.resource_names, request_store)]
        yield self.env.all_of(parallel_requests)
        self.service_time = np.random.uniform(self.time_min, self.time_max)
        print(f"{self.task_name} started at time {self.env.now:.2f}.")
        yield self.env.timeout(self.service_time)
        print(f"{self.task_name} completed in {self.service_time:.2f} minutes at time {self.env.now:.2f}.")
        for res, request in zip(self.resource_names, request_store):
            self.shared_resources[res].release(request)

    def request_resource_and_monitor_time(self, resource_to_request, request_process):
        start_time = self.env.now
        result = yield request_process | self.env.timeout(10000)
        if request_process in result:
            self.resource_wait_times[resource_to_request] = self.env.now - start_time
        else:
            self.resource_wait_times[resource_to_request] = float('inf')


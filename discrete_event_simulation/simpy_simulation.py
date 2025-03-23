import simpy
import random
import math
import pandas as pd
from .hospital_process import HospitalProcess

class SimpySimulation:
    '''
    Defines the skeletal framework for the specific problem (which is emergency department simulation).

    Dynamically coded (whereever possible) to accomodate future modifications and customisations to processes.

    The class consists of the following functions:
    
    1. __init__(resource_dict,  process_list, log_process_list,warmup_period =160*24*60):
        a. Used to initialise specific variables during class instantiation as an object.
           Here, the warmup period for this problem is set to 160 days, in terms of minutes.
    
    2. __begin__(until=360*24*60):
        a. Used to instantiate and simulate patients going through all the processes in the emergency
           department upto a specified time marker. Here, we assume 360 days in the problem, in terms of minutes.


    3. setup_resource_environment(env, resource_dict):
        a. Maps the given resource dictionary (defined by the user for the problem) into a simpy.resource dictionary
           for the environment to be able to allocate resources appropriately to each patient later on.
    
    4. patient_arrivals(env, resources):
        a. A simpy process that is used to model the pattern of arrival of patients. Randomly triggered on at a time
           interval selected from a random lognormal distribution with mean = 12.73 and sigma  = 6.16. Each instance
           of the process represents an individual patient arriving at the hospital.
    
    5. patient_process(env, patient_id, shared_resources,warmup_period):
        a. A simpy process that is used to run through all the emergency department processes for a specific patient,
           depending on the order of the specific process(es) and available resource(s) as instantiated by the user.

    6. data_collation():
        a. Converts the raw patient_log_data into an understandable dataframe, which can then be visualised to
           understand the patterns within the simulation output.
    
    7. store_data(name_of_file="CA1_A0313819B_data"):
        a. Converts the raw patient_log_data into an understandable dataframe (using the function above), and then
           writes the dataframe into a .csv file that can be accessed later on.


    The class has the following attributes:
        1. resource_dict: Dictionary that maps the available resource counts to the resources in the emergency department.
        2. process_list : A list of stages that the patient must go through during their visit to the emergency department.
        3. log_process_list : A list of stages for whom wait times must be recorded.
        4. warmup_period : The time taken to initialise the variables. The data generated before this time is not recorded.
        5. patient_log_data : A list of datapoints for all patients, consisting of their specific arrival times, wait times
           for each resource, and wait times for each specific process/stage to track.
        6. env : The SimPy environment.
        7. resources : A list of resources that are present in the environment (used mainly for processing tasks only).
    '''
    def __init__(self, resource_dict, process_list, log_process_list, warmup_period=160*24*60, until=360*24*60):
        self.resource_dict = resource_dict
        self.warmup_period = warmup_period
        self.process_list = process_list
        self.log_process_list = log_process_list
        self.patient_log_data = []
        self.resource_busy_time = {res: 0 for res in resource_dict}
        self.simulation_time = until

    def begin(self):
        self.env = simpy.Environment()
        self.resources = self.setup_resource_environment(self.env, self.resource_dict)
        self.env.process(self.patient_arrivals(self.env, self.resources))
        self.env.run(until=self.simulation_time)

    def setup_resource_environment(self, env, resource_dict):
        return {res: simpy.Resource(env, capacity=resource_dict[res]) for res in resource_dict}

    def patient_arrivals(self, env, resources):
        patient_id = 0
        while True:
            arrival_time = random.lognormvariate(math.log(12.73), math.log(6.16))
            yield env.timeout(arrival_time)
            env.process(self.patient_process(env, f"Patient {patient_id}", resources))
            patient_id += 1

    def patient_process(self, env, patient_id, shared_resources):
        print(f"Patient {patient_id} arrived at time {env.now:.2f}.")
        for process in self.process_list:
            current_stage = HospitalProcess(env, f"Patient {patient_id} - {process[0]}",
                                            process[1], tuple(process[2]), shared_resources)
            yield env.process(current_stage.run())

    def data_collation(self):
        df = pd.DataFrame(self.patient_log_data, columns=["patient_id", "arrival_time", "Total Time in ED"])
        return df

    def store_data(self, file_name="simulation_data.csv"):
        self.data_collation().to_csv(file_name, index=False)


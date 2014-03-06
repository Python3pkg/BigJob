import sys
import os
import time
import logging
#logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from pilot import PilotComputeService, PilotDataService, ComputeDataService, State


COORDINATION_URL = "redis://localhost:6379"

if __name__ == "__main__":      
    
    pilot_compute_service = PilotComputeService(coordination_url=COORDINATION_URL)

    # create pilot job service and initiate a pilot job
    pilot_compute_description = {
                             "service_url": 'fork://localhost',
                             "number_of_processes": 1,                             
                             "working_directory": os.getcwd() + "/work/",
                             'affinity_datacenter_label': "eu-de-south",              
                             'affinity_machine_label': "mymachine-1" 
                            }
    
    pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    
    
    # create pilot data service (factory for data pilots (physical, distributed storage))
    # and pilot data
    pilot_data_service = PilotDataService(coordination_url=COORDINATION_URL)
    pilot_data_description={
                                "service_url": "ssh://localhost/"+ os.getcwd() + "/pilot-data/",
                                "size": 100,   
                                "affinity_datacenter_label": "eu-de-south",              
                                "affinity_machine_label": "mymachine-1",
                             }
    
    pilot_data_service.create_pilot(pilot_data_description=pilot_data_description)
     
    compute_data_service = ComputeDataService()
    compute_data_service.add_pilot_compute_service(pilot_compute_service)
    compute_data_service.add_pilot_data_service(pilot_data_service)
    
    # Create Data Unit Description with list of files
    base_dir = "/Users/pmantha/papers/2013-hpc-bigdata/test/files"
    url_list = os.listdir(base_dir)
    # make absolute paths
    absolute_url_list = [os.path.join(base_dir, i) for i in url_list]
    print absolute_url_list
    data_unit_description = {
                              "file_urls": absolute_url_list,
                              "affinity_datacenter_label": "eu-de-south",              
                              "affinity_machine_label": "mymachine-1"
                             }    
      
    data_unit_description2 = {
                              "file_urls": [],
                              "affinity_datacenter_label": "eu-de-south",
                              "affinity_machine_label": "mymachine-1"
                             }
 
    # submit pilot data to a pilot store    
    data_unit = compute_data_service.submit_data_unit(data_unit_description)
    data_unit2 = compute_data_service.submit_data_unit(data_unit_description2)
    logging.debug("Submitted Data Unit: " + data_unit.get_url())
    logging.debug("Pilot Data URL: %s Description: \n%s"%(data_unit, str(pilot_data_description)))
    
    
    # start compute unit
    compute_unit_description = {
            "executable": "/bin/cat",
            "arguments": ["data_1-sorted-map-part-1"], 
            "number_of_processes": 1,
            "output": "stdout.txt",
            "error": "stderr.txt",   
            "input_data" : [{data_unit.get_url(): ["data_1-sorted-map-part-1"]}], # this stages the partial content of the data unit to the working directory of the compute unit
            "output_data": [
                            {
                             data_unit2.get_url(): 
                             ["std*"]
                            }
                           ],  
            "affinity_datacenter_label": "eu-de-south",              
            "affinity_machine_label": "mymachine-1" 
    }    
    
    
    
    compute_unit = compute_data_service.submit_compute_unit(compute_unit_description)
    logging.debug("Finished setup of PSS and PDS. Waiting for scheduling of PD")
    compute_data_service.wait()
    
    data_unit2.export(os.getcwd()+"/output")
    logging.debug("Terminate Pilot Compute/Data Service")
    compute_data_service.cancel()
    pilot_data_service.cancel()
    pilot_compute_service.cancel()

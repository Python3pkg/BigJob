import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.getcwd() + "/../")
from pilot import PilotComputeService, ComputeDataServiceDecentral, State

COORDINATION_URL = "redis://localhost:6379"

if __name__ == "__main__":      
    
    pilot_compute_service = PilotComputeService(coordination_url=COORDINATION_URL)

    # create pilot job service and initiate a pilot job
    pilot_compute_description = {
                             "service_url": 'subprocess://localhost',
                             "number_of_processes": 8,
                             "working_directory": os.path.join(os.getcwd(),"work"),
                            }
    
    pilotjob = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilotjob2 = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    
    compute_data_service = ComputeDataServiceDecentral()
    compute_data_service.add_pilot_compute_service(pilot_compute_service)
    
    # start work unit
    compute_unit_description = {
            "executable": "/bin/date",
            "number_of_processes": 1,
            "output": "stdout.txt",
            "error": "stderr.txt",
    }    

    cu_list = []
    for i in range(0,14):
        cu_list.append(compute_unit_description)

    compute_units = compute_data_service.submit_compute_unit_batch(cu_list)
    
    
    print("Finished setup. Waiting for scheduling of CU")
    compute_data_service.wait()

    compute_unit = compute_units[0]
    while compute_unit != State.Done:
        print("Final state check...")
        state_cu = compute_unit.get_state()
        print "PCS State %s" % pilot_compute_service
        print "CU: %s State: %s"%(compute_unit, state_cu)
        if state_cu==State.Done:
            break
        time.sleep(2)  
    
    print("Terminate Pilot Compute and Compute Data Service")
    compute_data_service.cancel()    
    pilot_compute_service.cancel()
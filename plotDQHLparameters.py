import os, errno
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
import json

def plotMeanRate(firstRun, lastRun):
    ########### GET MEAN RATE VALUES FROM TABLES ##########
    mean_rates = []
    run_numbers = []
    
    for runNum in range(firstRun, lastRun+1):
        fileName = "tables/DATAQUALITY_RECORDS_%i.ratdb"%runNum
        
        try:
            json_data = open(fileName).read()
            data = json.loads(json_data)
        except IOError as e:
            print "No RATDB file for run %i...skipping."%runNum
            continue
        else:
            print "RATDB file for run %i found. Assuming its "\
                "a PHYSICS run." % runNum
            mean_rates.append(data['checks']['dqtimeproc']['check_params']['mean_event_rate'])
            run_numbers.append(runNum)
    
    ########## MAKE THE PLOT ##########
    plt.plot(run_numbers, mean_rates, '.')
    plt.xlabel('Run number')
    plt.ylabel('Mean event rate')
    plt.title('Mean event rate over a range of runs')
    plt.grid(True)
    
    try:
        os.makedirs("plots")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    finally:
        plt.savefig("plots/mean_event_rate_%i-%i" % (firstRun, lastRun))

    return

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Get range of runs from two given run numbers")
    parser.add_argument("run_range", help="FIRSTRUN-LASTRUN", type=str)
    parser.add_argument("--download", help="Optional to download all the ratdb DATAQUALITY tables for the given run range.",
                        dest='downloadData', action='store_true', required=False)
    
    args = parser.parse_args()
    runs = args.run_range.split("-")
    parseOK = False
    if (len(runs) >= 1):
        if runs[0].isdigit():
            firstRun = int(runs[0])
            if len(runs) == 2:
                if runs[1].isdigit():
                    lastRun = int(runs[1])
                    parseOK = True
            elif len(runs) == 1:
                lastRun = firstRun
                parseOK = True
    if not parseOK:
        print parser.print_help()
        sys.exit(1)

    # Check firstrun < lastrun
    if(firstRun > lastRun):
        print "First run number must be lower or equal to the last run number."
        sys.exit(1)

    # Download data if optional argument provided
    if args.downloadData:
        from download_from_couchdb import download_physics_dq_data
        download_physics_dq_data(firstRun, lastRun)

    plotMeanRate(firstRun, lastRun)
    
    sys.exit(0)

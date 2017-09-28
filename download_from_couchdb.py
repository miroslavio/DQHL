#!/usr/bin/env python

# M. Mlejnek 28/9/17

import os, errno
import json
import couchdb
import sys
import DB_settings

# Some data quality tables include DQ runs that are not strictly physics runs
# Taken from Lisa's dqhlProcChecks.py code"
def isPhysicsRun(data):
    physicsRun = False
    if (data):
        checks = data['checks']
        if (('dqtellieproc' not in checks) and \
            ('dqsmellieprocproc' not in checks) and \
            ('dqtriggerproc' in checks) and \
            ('dqtimeproc' in checks) and \
            ('dqrunproc' in checks) and \
            ('dqpmtproc' in checks)):
            physicsRun = True
        
    return physicsRun

# For each run in the range given, download the DQ ratdb table into a file.
# Make sure first that the DQ table exists (i.e. its a DQ run) an make sure
# that it is a physics run.
def download_physics_dq_data(firstRun, lastRun):
    
    #################### CONNECT TO COUCHDB DQ SERVER ####################
    server = couchdb.Server(DB_settings.COUCHDB_SERVER)
    try:
        dqDB = server['data-quality']
    except:
        print "ERROR: Unable to access DB data-quality\n"
        sys.exit(1)
    ######################################################################

    #################### GET LIST OF DQTABLES FOR GIVEN RUNS ####################
    dqRunList = dqDB.view('_design/data-quality/_view/runs',
                          keys=range(firstRun, lastRun+1), include_docs=False)

    
    #################### FILTER THROUGH LIST FOR PHYSICS RUNS ####################
    for row in dqRunList:
        runNum = row.key
        data = dqDB.get(row['id'])
        
        if isPhysicsRun(data):
            outFile = "tables/DATAQUALITY_RECORDS_%i.ratdb" % runNum
            try:
                os.makedirs("tables")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            finally:
                fil = open(outFile, 'w')
                outString = json.dumps(data, fil, indent=1)
                fil.write(outString)
                fil.close()
    ##############################################################################
    
    return


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("run_range", help="FIRSTRUN-LASTRUN", type=str)
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

    print "Downloading data-quality tables for physics runs" \
          " in range %i-%i."%(firstRun, lastRun)
    
    download_physics_dq_data(firstRun, lastRun)

    sys.exit(0)

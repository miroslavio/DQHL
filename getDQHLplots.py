import argparse
import couchdb
import sys
import matplotlib.pyplot as plt
import numpy as np

#Connect to the couch database called dbName, return database
def getData(server, runNumber):
    #Accessing database
    try:
        dqDB = server['data-quality']
    except:
        print "Unable to access data quality database."
        sys.exit(1)
        
    data = None
    for row in dqDB.view('_design/data-quality/_view/runs'):
        if(int(row.key) == runNumber):
            runDocId = row['id']
            data = dqDB.get(runDocId)
            return data
    
def plotEventRate(x,y):
    plt.plot(x,y,'bo')
    plt.xlabel('Run number')
    locs = np.arange(min(x), max(x), 10)
    plt.xticks(locs, rotation=30)
    plt.gca().ticklabel_format(axis='x', useOffset=False)
    plt.ylabel('Mean event rate')
    plt.title('Mean event rate over a range of runs')
    plt.grid(True)
    plt.savefig('/home/miro/Software/DQ/plots/mean_event_rate_%i-%i'%(min(x),max(x)))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Get range of runs from two given run numbers")
    parser.add_argument('-i', type=int, required=True, help="First run number in your list.")
    parser.add_argument('-f', type=int, required=True, help="Last run number in your list.")
    args = parser.parse_args()

    firstRun = args.i
    lastRun = args.f
    #Check firstrun < lastrun
    if(firstRun > lastRun):
        print "First run number must be lower or equal to the last run number."
        sys.exit(1)

    #Connect to couchDB
    server = couchdb.Server("http://snoplus:dontestopmenow@couch.snopl.us")
    
    #Get dq info
    x = range(firstRun, lastRun+1)
    y = []
    for run in range(firstRun, lastRun+1):
        data = getData(server, run)
        if data!=None:
            y.append(data['checks']['dqtimeproc']['check_params']['mean_event_rate'])
        else:
            x.remove(run)
    plotEventRate(x,y)

    sys.exit(0)

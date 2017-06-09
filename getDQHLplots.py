from download_from_couchdb import download_from_couchdb
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

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

    #Download data from couchdb for data quality
    print "Downloading data from couchdb for runs %i-%i\n"%(firstRun,lastRun)
    data = download_from_couchdb("data-quality", firstRun, lastRun)

    sys.exit(0)

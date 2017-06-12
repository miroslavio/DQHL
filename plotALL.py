import matplotlib.pyplot as plt



def plotTrigger(data, runs):
    x = runs
    y = []
    for run in data:
        y.append(run['checks']['dqtimeproc']['check_params']['mean_event_rate'])
    plt.plot(x,y,'bo')
    plt.show()













# Input is a data dictionary produced by download_from_couchdb
def plotALL(data, runs):
    plotTrigger(data, runs)
    

def print_values(data):
    data = data['checks']

    print "Time processor check results:\n", data['dqtimeproc']
    print "Run processor check results:\n", data['dqrunproc']
    print "Trigger processor check results:\n", data['dqtriggerproc']
    print "PMT processor check results:\n", data['dqpmtproc']    
    

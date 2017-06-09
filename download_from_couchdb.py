import couchdb
import sys
import DB_settings

def download_from_couchdb(dbName, firstRun, lastRun):
    server = couchdb.Server(DB_settings.COUCHDB_SERVER)
    try:
        dqDB = server[dbName]
    except:
        print "Unable to access DB: %s\n"%dbName
        sys.exit(1)

    # Data dictionary, keys are run numbers and values are data quality check parameters
    data = {}
    for runNumber in range(firstRun, lastRun+1):
        for row in dqDB.view('_design/data-quality/_view/runs'):
            if(int(row.key) == runNumber):
                runDocId = row['id']
                data[runNumber] = dqDB.get(runDocId)
    return data

if __name__=="__main__":
    download_from_couchdb("data-quality", 101054, 101056)

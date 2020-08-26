########################################################################################
"""db_interface.py provides basic tools for communication with an influxdb database"""
########################################################################################


from influxdb import InfluxDBClient


########################################################################################


def extractdatahist(client,sensorselec,fieldselec,xrange):
    """Returns data from a client as tuple"""
    res=client.query('select * from "log" where time <='+xrange[1]+' and time >='+xrange[0])
    points=res.get_points(tags={'sensor':sensorselec})
    d=[]
    t=[]
    
    for i in points:
        d.append(i[fieldselec])
        t.append(i['time'])
        
    return t, d


def fieldlabels(client,sensorselec,xrange):
    """Returns list of sensor field labels in database."""
    res=client.query('select * from "log" where time <='+xrange[1]+' and time >='+xrange[0])
    points=res.get_points(tags={'sensor':sensorselec})
    f=[]
    for point in points:
        for key in point.keys():
            if key!='time' and key!='type' and key!='sensor':
                if key not in f:
                    f.append(key)
    return f


def sensorsindb(client,type):
    """Returns a list of all sensors of a certain type from client."""
    res=client.query('SELECT * FROM "log"')
    points=res.get_points(tags={'type':type})
    l=[]
    for i in points:
        if i['sensor'] not in l:
            l.append(i['sensor'])

    return l
            

def initiatedb(db="DB",host="localhost",port=8086):
    """Returns a client with the active Database DB"""
    client=InfluxDBClient(host,port)
    #Note that client.create_database(db) does nothing if the Database db already exists
    client.create_database(db)
    client.switch_database(db)
    return client

    





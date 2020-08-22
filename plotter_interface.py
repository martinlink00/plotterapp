#####################################################################################################################
"""plotter_interface.py provides necessary tools for the plotter app to recieve and plot data from the influxdb"""
#####################################################################################################################



import db_interface as db
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


#####################################################################################################################



class Guiinterfaceplotter:
    """This class provides tools for the GUI to plot data from the database"""
    def __init__(self,database="DB",host="localhost",port=8086):
        self._beamviewer=Beamviewer()
        self._tempviewer=Tempviewer()
        self._client=db.initiatedb(database,host,port)
        
        self.camexportcounter=0
        self.tempexportcounter=0
        self.beamsindb=db.sensorsindb(self._client,'camera')
        self.tempindb=db.sensorsindb(self._client,'temperature')
        

    
    
    def selectbeam(self,beamselec):
        if beamselec in self.beamsindb:
            self._beamviewer.setselectedbeam(beamselec)
            
            
    def selecttemp(self,tempselec):
        if tempselec in self.tempindb:
            self._tempviewer.setselectedtemp(tempselec)
            
        
    
    def plotbeamgraph(self,fields,xran):
         
        """Plots selected field data from active beam sensor over duration from xrange[0] to xrange[1]"""
        xrange=['','']
        
        if xran[1] is None:
            xrange[1]='now()'
        else:
            xrange[1]=xran[1]
        if xran[0] is None:
            xrange[0]=xrange[1] + '-1d'
        else:
            xrange[0]=xran[0]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        for field in fields:
            xl=self._beamviewer.getplotdata(self._client,field,xrange)[0]
            yl=self._beamviewer.getplotdata(self._client,field,xrange)[1]
            if field=="angle":
                fig.add_trace(go.Scatter(x=xl,y=yl, mode="lines",name=field),secondary_y=True)
            else:
                fig.add_trace(go.Scatter(x=xl,y=yl, mode="lines",name=field),secondary_y=False)
            
        fig.update_yaxes(title_text="Distance [μm]", secondary_y=False)
        fig.update_yaxes(title_text="Angle [°]", secondary_y=True)
        return fig
    
    def plottempgraph(self,xran):
        """Plots selected field data from active temp sensor over duration from xrange[0] to xrange[1]"""
        xrange=['','']
        
        if xran[1] is None:
            xrange[1]='now()'
        else:
            xrange[1]=xran[1]
        if xran[0] is None:
            xrange[0]=xrange[1] + '-1d'
        else:
            xrange[0]=xran[0]
        
        fields=['channel' + str(i+1) for i in range(0,9)]
        
        fig = go.Figure()
        
        for field in fields:
            xl=self._tempviewer.getplotdata(self._client,field,xrange)[0]
            yl=self._tempviewer.getplotdata(self._client,field,xrange)[1]
            fig.add_trace(go.Scatter(x=xl,y=yl, mode="lines",name=field))
        fig.update_yaxes(title_text="Temperature [°C]")
        
        return fig

    
    def writedatfile_cam(self,path,fields,xran):
        """Writes one dat file for each beam-field selected. If xran[0] is None, one day will be exported, If xran[1] is None, it will be set to the current time (meaning that if both are None, the last day will be exported)."""
        
        xrange=['','']

        if xran[1] is None:
            xrange[1]='now()'
        else:
            xrange[1]=xran[1]
        if xran[0] is None:
            xrange[0]=xrange[1] + '-1d'
        else:
            xrange[0]=xran[0]

        if fields is not None and path is not None:
            exportto=path+'datalogger_export'
            for field in fields:
                try:
                    dat={}
                    dat['Time']=self._beamviewer.getplotdata(self._client,field,xrange)[0]
                    dat[field]=self._beamviewer.getplotdata(self._client,field,xrange)[1]
                    output_df=pd.DataFrame(data=dat)
                    output_df.to_csv(exportto+'-'+field+'.dat',index=False,sep='\t')
                    print("A DAT-File was saved as "+exportto+'-'+field+'.dat')
                except:
                    print("Error while exporting "+exportto+'-'+field+'.dat')


        self.beamexportcounter += 1
        
        
    def writedatfile_temp(self,path,xran):
        """Writes one dat file for each temp-field selected. If xran[0] is None, one day will be exported, If xran[1] is None, it will be set to the current time (meaning that if both are None, the last day will be exported)."""
        
        xrange=['','']

        if xran[1] is None:
            xrange[1]='now()'
        else:
            xrange[1]=xran[1]
        if xran[0] is None:
            xrange[0]=xrange[1] + '-1d'
        else:
            xrange[0]=xran[0]

        fields=['channel' + str(i+1) for i in range(0,9)]
        
        if path is not None:
            exportto=path+'datalogger_export'
            for field in fields:
                try:
                    dat={}
                    dat['Time']=self._tempviewer.getplotdata(self._client,field,xrange)[0]
                    dat[field]=self._tempviewer.getplotdata(self._client,field,xrange)[1]
                    output_df=pd.DataFrame(data=dat)
                    output_df.to_csv(exportto+'-'+field+'.dat',index=False,sep='\t')
                    print("A DAT-File was saved as "+exportto+'-'+field+'.dat')
                except:
                    print("Error while exporting "+exportto+'-'+field+'.dat')


        self.tempexportcounter += 1
        


    
    
class Beamviewer:
    def __init__(self):
        self._selectedbeam=None
        self._hasactivebeam=False
        
    def setselectedbeam(self,sensorid):
        if self._selectedbeam!=sensorid:
            self._selectedbeam=sensorid
            self._hasactivebeam=True
     
    def getplotdata(self,client,field,xrange):
        return db.extractdatahist(client,self._selectedbeam,field,xrange)
    
    

class Tempviewer:
    def __init__(self):
        self._selectedtemp=None
        self._hasactivetemp=False
        
    def setselectedtemp(self,sensorid):
        if self._selectedtemp!=sensorid:
            self._selectedtemp=sensorid
            self._hasactivetemp=True
     
    def getplotdata(self,client,field,xrange):
        return db.extractdatahist(client,self._selectedtemp,field,xrange)
            
    
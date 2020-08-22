###############################################################################
"""This is the main GUI app used to plot and analyse data from the database"""
###############################################################################

#Note that no camera needs to be connected to the computer, in order to use this app. 
#All it does is extract data from the influxdb database and plot it.
#This was done intentionally, so that maybe the influx Database can be run on a remote server.

from datetime import datetime as dt
from datetime import timedelta
import time

import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotter_interface as im


###############################################################################


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

guiintplot=im.Guiinterfaceplotter()

if len(guiintplot.beamsindb)!=0 and len(guiintplot.tempindb)!=0:
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Beam Data Analysis'),
                html.Div([
                    dcc.Dropdown(
                        id='beam-selection',
                        options=[{'label': i, 'value': i} for i in guiintplot.beamsindb],
                        value=guiintplot.beamsindb[0]

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_cam',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='beamgraph'
                    ),
                    dcc.Checklist(
                        id='field-selection',
                        options=[{'label': 'Horizontal position', 'value': 'hcenter'},
                                 {'label': 'Vertical position', 'value': 'vcenter'},
                                 {'label': 'Waist (large axis)', 'value': 'largewaist'},
                                 {'label': 'Waist (small axis)', 'value': 'smallwaist'},
                                 {'label': 'Angle','value':'angle'}
                                ],
                        value=['hcenter', 'vcenter','largewaist','smallwaist','angle'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_cam",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_cam', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_cam"),
                    ]),
                    dcc.Interval(
                    id='interval-beam',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                    )
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'}),


            ],style={'width': '95%','height':'95%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Temperature Data Analysis'),
                html.Div([ 
                    dcc.Dropdown(
                        id='temp-selection',
                        options=[{'label': i, 'value': i} for i in guiintplot.tempindb],
                        value=guiintplot.tempindb[0]

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_temp',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(250,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='tempgraph'
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_temp",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_temp', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_temp"),
                    ]),
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'})

            ],style={'width': '95%','height':'95%', 'display': 'inline-block'})



        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px',
            'columnCount':2
        }),



    ], style={'columnCount': 1}
    )

elif len(guiintplot.beamsindb)!=0 and len(guiintplot.tempindb)==0:
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Beam Data Analysis'),
                html.Div([
                    dcc.Dropdown(
                        id='beam-selection',
                        options=[{'label': i, 'value': i} for i in guiintplot.beamsindb],
                        value=guiintplot.beamsindb[0]

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_cam',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='beamgraph'
                    ),
                    dcc.Checklist(
                        id='field-selection',
                        options=[{'label': 'Horizontal position', 'value': 'hcenter'},
                                 {'label': 'Vertical position', 'value': 'vcenter'},
                                 {'label': 'Waist (large axis)', 'value': 'largewaist'},
                                 {'label': 'Waist (small axis)', 'value': 'smallwaist'},
                                 {'label': 'Angle','value':'angle'}
                                ],
                        value=['hcenter', 'vcenter','largewaist','smallwaist','angle'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_cam",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_cam', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_cam"),
                    ]),
                    dcc.Interval(
                    id='interval-beam',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                    )
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'}),


            ],style={'width': '95%','height':'95%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Temperature Data Analysis'),
                html.Div([ 
                    dcc.Dropdown(
                        id='temp-selection',
                        disabled=True

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_temp',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='tempgraph'
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_temp",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_temp', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_temp"),
                    ]),
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'})

            ],style={'width': '95%','height':'95%', 'display': 'inline-block'})



        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px',
            'columnCount':2
        }),



    ], style={'columnCount': 1}
    )
    
elif len(guiintplot.beamsindb)==0 and len(guiintplot.tempindb)!=0:
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Beam Data Analysis'),
                html.Div([
                    dcc.Dropdown(
                        id='beam-selection',
                        disabled=True

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_cam',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='beamgraph'
                    ),
                    dcc.Checklist(
                        id='field-selection',
                        options=[{'label': 'Horizontal position', 'value': 'hcenter'},
                                 {'label': 'Vertical position', 'value': 'vcenter'},
                                 {'label': 'Waist (large axis)', 'value': 'largewaist'},
                                 {'label': 'Waist (small axis)', 'value': 'smallwaist'},
                                 {'label': 'Angle','value':'angle'}
                                ],
                        value=['hcenter', 'vcenter','largewaist','smallwaist','angle'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_cam",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_cam', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_cam"),
                    ]),
                    dcc.Interval(
                    id='interval-beam',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                    )
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'}),


            ],style={'width': '95%','height':'95%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Temperature Data Analysis'),
                html.Div([ 
                    dcc.Dropdown(
                        id='temp-selection',
                        options=[{'label': i, 'value': i} for i in guiintplot.tempindb],
                        value=guiintplot.tempindb[0]

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_temp',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='tempgraph'
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_temp",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_temp', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_temp"),
                    ]),
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'})

            ],style={'width': '95%','height':'95%', 'display': 'inline-block'})



        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px',
            'columnCount':2
        }),



    ], style={'columnCount': 1}
    )

else:
    
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H3('Beam Data Analysis'),
                html.Div([
                    dcc.Dropdown(
                        id='beam-selection',
                        disabled=True

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_cam',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='beamgraph'
                    ),
                    dcc.Checklist(
                        id='field-selection',
                        options=[{'label': 'Horizontal position', 'value': 'hcenter'},
                                 {'label': 'Vertical position', 'value': 'vcenter'},
                                 {'label': 'Waist (large axis)', 'value': 'largewaist'},
                                 {'label': 'Waist (small axis)', 'value': 'smallwaist'},
                                 {'label': 'Angle','value':'angle'}
                                ],
                        value=['hcenter', 'vcenter','largewaist','smallwaist','angle'],
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_cam",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_cam', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_cam"),
                    ]),
                    dcc.Interval(
                    id='interval-beam',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
                    )
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'}),


            ],style={'width': '95%','height':'95%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Temperature Data Analysis'),
                html.Div([ 
                    dcc.Dropdown(
                        id='temp-selection',
                        disabled=True

                    ),
                    html.Div('Select time range: (the last day is portrayed if nothing is selected)'),
                    dcc.DatePickerRange(
                        id='rangepicker_temp',
                        clearable=True,
                        min_date_allowed=dt(2020, 4, 1),
                        max_date_allowed=dt(2050,1,1)#fromtimestamp(time.time()),
                    ),
                    dcc.Graph(
                    id='tempgraph'
                    ),
                    html.Div([
                        ##Export region
                        html.H3('Export to ".dat" file:'),
                        dcc.Input(
                            id="path-input_temp",
                            type='text',
                            value='/home/martinl/',
                            placeholder="Export destination",
                            style={'width': '100%'}),
                        html.Button(id='export-button_temp', n_clicks=0, children='Submit'),
                        html.Div(id="button-div_temp"),
                    ]),
                ],
                style={'width': '95%','height':'95%', 'display': 'inline-block'})

            ],style={'width': '95%','height':'95%', 'display': 'inline-block'})



        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px',
            'columnCount':2
        }),



    ], style={'columnCount': 1}
    )
    
    

@app.callback(
    [dash.dependencies.Output('beamgraph', 'figure'),
    dash.dependencies.Output('tempgraph', 'figure')],
    [dash.dependencies.Input('beam-selection', 'value'),
    dash.dependencies.Input('temp-selection', 'value'),
    dash.dependencies.Input('field-selection', 'value'),
    dash.dependencies.Input('interval-beam', 'n_intervals'),
    dash.dependencies.Input('rangepicker_cam', 'start_date'),
    dash.dependencies.Input('rangepicker_cam', 'end_date'),
    dash.dependencies.Input('rangepicker_temp', 'start_date'),
    dash.dependencies.Input('rangepicker_temp', 'end_date')])


def update_graphs(beamselection,tempselection,fieldselection,n,startdatecam,enddatecam,startdatetemp,enddatetemp):
    guiintplot.selectbeam(beamselection)
    guiintplot.selecttemp(tempselection)
    
    if startdatecam is not None:
        timestcam="'"+startdatecam+"'"
    else:
        timestcam=None
    if enddatecam is not None:
        timeencam="'"+enddatecam+"'"+"+1d" #The 1d was necessary in order to include the whole 'end date' in the query
    else:
        timeencam=None
    
    
    if startdatetemp is not None:
        timesttemp="'"+startdatetemp+"'"
    else:
        timesttemp=None
    if enddatetemp is not None:
        timeentemp="'"+enddatetemp+"'"+"+1d" #The 1d was necessary in order to include the whole 'end date' in the query
    else:
        timeentemp=None
        
    
    return guiintplot.plotbeamgraph(fieldselection,[timestcam,timeencam]), guiintplot.plottempgraph([timesttemp,timeentemp])



@app.callback(
    dash.dependencies.Output('button-div_cam','children'),
    [dash.dependencies.Input('export-button_cam', 'n_clicks'),
    dash.dependencies.Input('field-selection', 'value'),
    dash.dependencies.Input('rangepicker_cam', 'start_date'),
    dash.dependencies.Input('rangepicker_cam', 'end_date')],
    [dash.dependencies.State('path-input_cam', 'value')]
)


def onexportbuttoncam(n_clicks,fieldselection,startdate,enddate,path):
    if guiintplot.camexportcounter<n_clicks:
        if startdate is not None:
            timest="'"+startdate+"'"
        else:
            timest=None
        if enddate is not None:
            timeen="'"+enddate+"'"+"+1d" #The 1d was necessary in order to include the whole 'end date' in the query
        else:
            timeen=None
        
        guiintplot.writedatfile_cam(path,fieldselection,[timest,timeen])
        
    return "Pressing the button will export one DAT-File for each trace you can see in the plot above."
 
    
@app.callback(
    dash.dependencies.Output('button-div_temp','children'),
    [dash.dependencies.Input('export-button_temp', 'n_clicks'),
    dash.dependencies.Input('rangepicker_temp', 'start_date'),
    dash.dependencies.Input('rangepicker_temp', 'end_date')],
    [dash.dependencies.State('path-input_temp', 'value')]
)


def onexportbuttontemp(n_clicks,startdate,enddate,path):
    if guiintplot.tempexportcounter<n_clicks:
        if startdate is not None:
            timest="'"+startdate+"'"
        else:
            timest=None
        if enddate is not None:
            timeen="'"+enddate+"'"+"+1d" #The 1d was necessary in order to include the whole 'end date' in the query
        else:
            timeen=None
        
        guiintplot.writedatfile_temp(path,[timest,timeen])
        
    return "Pressing the button will export one DAT-File for each trace you can see in the plot above."




if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
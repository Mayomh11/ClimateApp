from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt


# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Calculate the date 1 year ago from the last data point in the database
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """ List of available API"""
    return (
        
        f"Welcome to Hawai APi<br/>"        
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
        
#Convert the query results to a Dictionary using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    
    greatestdate = dt.date(2017, 8, 23)
    months_list = session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date >= greatestdate).all()
    months_dict = dict()
    [months_dict [t [0]].append(t [1]) if t [0] in list(months_dict.keys()) 
    else months_dict.update({t [0]: [t [1]]}) for t in months_list]
    return jsonify(months_dict)
    
    

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations<br/>")
def stations():
    unique_stations = session.query(Measurement.station).distinct().all()
    return jsonify(unique_stations)
                

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.                   

@app.route("/api/v1.0/tobs<br/>")
def temperature_observations():
    """
     query for the dates and temperature observations from a year from the last data point.
     """
    temperature_tobs = session.query(Measurements.tobs).\
        filter(Measurement.tobs > prev_year).\
        all()
    return jsonify(temperature_tobs)
                   
                   
#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.              
                   
@app.route("/api/v1.0/<start>")              
def start(date):
    Starting_temperature = "select date, min(tobs), avg(tobs), max(tobs)\
        from Measurement where date >= '" + date + "' group by date"
    Start_temperature_List = pd.read_sql_query(Starting_temperature)
    Start_temperature_List = [tuple(x) for x in Start_temperature_List.values]
    Start_temperature_dict = {}
    for temp in Start_temp_List:
        Temps = { 'MinTemp': temp[1], 'AvgTemp': i[2], 'MaxTemp':temp[3]}
        Start_temperature_dict[temp[0]] = Temps
    return jsonify(Start_temperature_dict) 
                   
                
                   
                   
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
     TempStatQ = "select date, min(tobs), avg(tobs), max(tobs)\
               from Measurement where date >= '" + start + "' and \
               date <='" + end + "' group by date"                    
     Start_temperature_List = pd.read_sql_query(Starting_temperature)
     Start_temperature_List = [tuple(x) for x in Start_temperature_List.values]
     Start_temperature_dict = {}
     for temp in Start_temp_List:
         Temps = { 'MinTemp': temp[1], 'AvgTemp': i[2], 'MaxTemp':temp[3]}
         Start_temperature_dict[temp[0]] = Temps
     return jsonify(Start_temperature_dict) 
         


if __name__ == "__main__":
    app.run(debug=True)

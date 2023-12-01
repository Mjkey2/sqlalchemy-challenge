# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Start at the homepage "/"                  CHECK
    #homepage
    #list all available routes
#precipitation                              CHECK
    #convert query results from precipitation analysis to a dictionary using date as the key and prcp as the value
    #return json representation of the dictionary
#stations
    #return JSON list of stations from the dataset
#tobs
    #query the dates and temperature observations of the most active station (USC00519281) from previous year (12 months) of date
    #return a JSON list of temperature observaitions for the previous year (12 months)
#<start> (SPECIFIED START)
    #return a json list of MINIMUM TEMPERATURE, the AVERAGE TEMPERATURE, and MAXIMUM TEMPERTURE for specified start or start-end ranges
    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#<start>/<end> (SPECIFIED START AND END)
    #return a json list of MINIMUM TEMPERATURE, the AVERAGE TEMPERATURE, and MAXIMUM TEMPERTURE for specified start or start-end ranges
    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive

#Start at the homepage "/"     
#homepage
@app.route("/")
def welcome():
    #list all available routes
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"Precipitation Values: /api/v1.0/precipitation<br/>"
        f"List of Weather Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations: /api/v1.0/tobs<br/>"
        f"Temperature statistics from a start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature statistics from start and end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    ) 

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    sel = [Measurement.date,Measurement.prcp]
    queryresult = session.query(*sel).all()
    #close
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    precipitaton_query_values = []
    # Create for loop to iterate through query results
    for prcp, date in precipitaton_query_values:
        precipitation_dict = {}
        #Create dictionary with key "precipitation" set to prcp from precipitation_query_results and key "date" to date from precipitation_query_results
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        # Append values from precipitation_dict to your original empty list precipitation_query_values 
        precipitaton_query_values.append(precipitation_dict)

        #Return JSON format of your new list that now contains the dictionary of prcp and date values to your browser
        return jsonify(precipitaton_query_values) 
    
# Create a route that returns a JSON list of stations from the database
@app.route("/api/v1.0/stations")
def station(): 
    #create session
    session = Session(engine)

    station_query_results = session.query(Station.station,Station.id).all()
    session.close()  

    #make and return a JSON list of stations from the dataset.
    stations_values = []
    for station, id in station_query_results:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_values.append(stations_values_dict)
    return jsonify (stations_values) 

@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)
    
    #query the dates and temperature observations for the last 12 months of the most active station (USC00519281)
    start_date = '2016-08-23'
    sel = [Measurement.date, 
           Measurement.tobs]
        # check if station name is same as jupyter notebook name
    station_temps = session.query(*sel).filter(Measurement.date >= start_date, Measurement.station == 'USC00519281').group_by(Measurement.date).order_by(Measurement.date).all()
    
    session.close()

    # return a dict with date as key and daily tobs as value
    observation_dates = []
    temperature_observations = []

    for date, observation in station_temps:
        observation_dates.append(date)
        temperature_observations.append(observation)
    
    most_active_tobs_dict = dict(zip(observation_dates, temperature_observations))

    return jsonify(most_active_tobs_dict)

@app.route("/api/v1.0/trip/start")
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    #return json list of min avg and max temperature for specified start date
    return jsonify(tobsall)

@app.route('/api/v1.0/<start>/<stop>')
def get_t_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    #return json list of min avg and max temperature for specified start and end dates
    return jsonify(tobsall)
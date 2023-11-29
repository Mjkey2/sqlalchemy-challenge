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

#create root route
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"Precipitation Totals Year Span: /api/v1.0/precipitation<br/>"
        f"List of Weather Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
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
    """Return a list of stations from the database""" 
    station_query_results = session.query(Station.station,Station.id).all()

    session.close()  
    stations_values = []
    for station, id in station_query_results:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_values.append(stations_values_dict)
    return jsonify (stations_values) 
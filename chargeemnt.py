
import pandas as pd
from sqlalchemy import create_engine

root = 'root'
password = ''

engine = create_engine(f'mysql+pymysql://{root}:{password}@localhost/chat')

# Process the CSV file in chunks
chunksize = 10000
for chunk in pd.read_csv('clean_flights.csv', chunksize=chunksize, dtype={
    'YEAR': 'int16',
    'MONTH': 'int8',
    'DAY': 'int8',
    'DAY_OF_WEEK': 'int8',
    'AIRLINE': 'category',
    'FLIGHT_NUMBER': 'int32',
    'TAIL_NUMBER': 'category',
    'ORIGIN_AIRPORT': 'category',
    'DESTINATION_AIRPORT': 'category',
    'SCHEDULED_DEPARTURE': 'int16',
    'DEPARTURE_TIME': 'float32',
    'DEPARTURE_DELAY': 'float32',
    'TAXI_OUT': 'float32',
    'WHEELS_OFF': 'float32',
    'SCHEDULED_TIME': 'float32',
    'ELAPSED_TIME': 'float32',
    'AIR_TIME': 'float32',
    'DISTANCE': 'float32',
    'WHEELS_ON': 'float32',
    'TAXI_IN': 'float32',
    'SCHEDULED_ARRIVAL': 'int16',
    'ARRIVAL_TIME': 'float32',
    'ARRIVAL_DELAY': 'float32',
    'DIVERTED': 'int8',
    'CANCELLED': 'int8',
    'PRICE': 'float32'
}):
    chunk.to_sql('vols', con=engine, if_exists='append', index=False)
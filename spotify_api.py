import requests
import time
import pandas as pd
import datetime
import pytz
import sqlalchemy as db


def get_recently_played_tracks(token,days):
    days = 1
    curr_time = time.time() # Time since epoch
    tiempo = curr_time - (86400 * days)
    tiempo_ml = int(tiempo  * 1000)
    # Convert milliseconds to seconds
    seconds_timestamp = tiempo_ml / 1000
    # Create a datetime object from the seconds timestamp
    dt_object = datetime.datetime.fromtimestamp(seconds_timestamp)
    # Format the datetime object as a string in the desired format
    formatted_datetime = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    print(f'Get all the songs played in Spotify after ---- > {formatted_datetime}')
    parametros= {'limit': 50, 'after': tiempo_ml}
    headers = {'Authorization': 'Bearer {}'.format(token)}
    endpoint = 'https://api.spotify.com/v1/me/player/recently-played'
    response = requests.get(endpoint, headers=headers,params=parametros)
    return response.json(),response.status_code

def sort_data(music_played):
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    for song in music_played['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
    
    song_dict = {
        "song_name":song_names,
        "artist_name":artist_names,
        "played_at":played_at_list,
        "timestamp":timestamps
    }
    return song_dict

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs donwloaded. Finishing execution")
        return False
    
    # Primary Key check, check if played_at is unique
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")
    
    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null vauled founded")
    
    # Check that all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0) #2023-07-25 00:00:00 Put 00 in hour ,minute,second and microsecond to comparate

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if not timestamp >= yesterday: #Comparte yesterday that the format is 2023-07-25 00:00:00  and timestamp that the format is 023-07-25 # T
            raise Exception("At least one of the returned songs does not come from within the last 24 hours")
    
    print(df)
    return True

def transform_data(song_dictionary):
    song_df = pd.DataFrame(song_dictionary,columns = ["song_name","artist_name","played_at","timestamp"])

    # Assuming the original timestamps are in UTC
    utc_timezone = pytz.timezone('UTC')
    colombian_timezone = pytz.timezone('America/Bogota')

    #Convert the 'timestamp' column to datetime
    song_df['timestamp'] = pd.to_datetime(song_df['timestamp'])

    # Convert the 'played_at' column to datetime and localize it to UTC
    song_df['played_at'] = pd.to_datetime(song_df['played_at']).dt.tz_convert(utc_timezone)

    # Convert the 'played_at' column to the Colombian time zone
    song_df['played_at_timezone_colombia'] = song_df['played_at'].dt.tz_convert(colombian_timezone)

    return song_df


def uploadData(song_df):
    # Replace the following variables with your PostgreSQL credentials
    username = 'postgres'
    password = 'Guerrero99134'
    host = 'localhost'
    port = '5433'
    database_name = 'spotify_tracks'

    # Create a connection string for the default 'postgres' database
    connection_string = f"postgresql://{username}:{password}@{host}:{port}/postgres"

    # Connect to the default 'postgres' database
    engine = db.create_engine(connection_string, connect_args={"connect_timeout": 10})

    try:
        connection = engine.connect()
        if connection:
            # Check if the 'spotify_tracks' database exists
            database_exists_query = f"SELECT 1 FROM pg_database WHERE datname = '{database_name}';"
            result = connection.execute(database_exists_query).fetchone()

            if not result:
                # Set isolation level to autocommit mode
                connection.execution_options(isolation_level="AUTOCOMMIT")
                # Create the 'spotify_tracks' database
                create_database_query = f"CREATE DATABASE {database_name};"
                connection.execute(create_database_query)
                print(f"Created database '{database_name}' successfully.")
            else:
                print(f"Database '{database_name}' already exists.")

            # Close the connection to the default 'postgres' database
            connection.close()

            try:
                # Create a connection string for the 'spotify_tracks' database
                connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
                # Connect to the 'spotify_tracks' database
                engine = db.create_engine(connection_string, connect_args={"connect_timeout": 10})

                connection = engine.connect()
                if connection:
                    # Create table in the 'spotify_tracks' database
                    sql_query = """
                    CREATE TABLE IF NOT EXISTS my_played_tracks(
                    song_name VARCHAR(255) NOT NULL,
                    artist_name VARCHAR(200),
                    played_at TIMESTAMP WITH TIME ZONE,
                    timestamp VARCHAR(200),
                    played_at_timezone_colombia TIMESTAMP WITH TIME ZONE,
                    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
                    )
                    """
                    connection.execute(sql_query)
                    print("Table 'my_played_tracks' created successfully.")
                

            except Exception as table_creation_error:
                print(f"Table creation failed: {table_creation_error}")
            
            #Upload the data to the table 'my_played_tracks'
            try:
                song_df.to_sql('my_played_tracks',connection,index=False,if_exists='append')
                print("Successfully data load")
            except Exception as e:
                print(f"Data already exists in the database: {e}")
            
            #Close the connection of the database 'spotify_tracks'
            connection.close()
            print('Close the database successfully')



    except Exception as e:
        print(f'Connection failed: {e}')







if __name__ == '__main__':
    # Get the token that is in the access_token.txt
    with open('access_token.txt', 'r') as f:
        token = f.read()
    music_played,status_code = get_recently_played_tracks(token,1) #Use the token and invoked the function to get the data in a window of 1 day until current time
    
    

    if status_code == 200: 
        song_playlist = sort_data(music_played)
        song_df = transform_data(song_playlist)
        check_if_valid_data(song_df)
        print('Data valid, proceed to Load Stage')
        if check_if_valid_data:
            uploadData(song_df)


    else:
        print(f'Response: {music_played}')

    




   
    
    

  



    


    

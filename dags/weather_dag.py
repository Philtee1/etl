from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def kelvin_to_fahrenheit(temp_in_kelvin):
    """Convert temperature from Kelvin to Fahrenheit."""
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit 

def transform_load_data(task_instance):
    try:
        # Pull the extracted data from the previous task
        data = task_instance.xcom_pull(task_ids='extract_weather_data')
        if not data:
            raise ValueError("No data retrieved from the API")

        # Extract necessary fields from the API response
        city = data["name"]
        weather_description = data["weather"][0]["description"]
        temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp"])
        feels_like_fahrenheit = kelvin_to_fahrenheit(data["main"]["feels_like"])
        min_temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
        max_temp_fahrenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        time_of_record = datetime.utcfromtimestamp(data["dt"] + data['timezone'])
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

        # Create a dictionary for transformed data
        transformed_data = {
            "City": city,
            "Description": weather_description,
            "Temperature (F)": temp_fahrenheit,
            "Feels like (F)": feels_like_fahrenheit,
            "Minimum Temp (F)": min_temp_fahrenheit,
            "Maximum Temp (F)": max_temp_fahrenheit,
            "Pressure": pressure,
            "Humidity": humidity,
            "Wind Speed": wind_speed,
            "Time of Record": time_of_record,
            "Sunrise (Local Time)": sunrise_time,
            "Sunset (Local Time)": sunset_time 
        }

        # Convert the dictionary to a DataFrame
        df_data = pd.DataFrame([transformed_data])

        # Get AWS credentials from environment variables
        aws_credentials = {
            "keyId": f"{os.getenv('AccessKeyId')}",
            "secret": f"{os.getenv('SecretAccessKey')}",
            "token": f"{os.getenv('SessionToken')}"
        }

        # Generate a unique filename based on the current date and time
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        filename = f"current_weather_data_portland_{dt_string}.csv"

        # Save the DataFrame to an S3 bucket
        df_data.to_csv(f"s3://airflowweatherapibucket/{filename}", index=False, storage_options=aws_credentials)

    except Exception as e:
        print(f"Error in transform_load_data: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 3),
    'email': ['samaphil02@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG('weather_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    # HttpSensor to first check if the API is available and working
    weather_api_readiness = HttpSensor(
        task_id='weather_api_readiness',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=b3f2e7f8ab423fd0c04f940d301540bc'
    )
    
    # Extract the JSON weather data from the connection
    extract_weather_data = SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=b3f2e7f8ab423fd0c04f940d301540bc',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    # Transforming the extracted data
    transform_load_weather_data = PythonOperator(
        task_id='transform_load_weather_data',
        python_callable=transform_load_data
    )

    # Task dependencies
    weather_api_readiness >> extract_weather_data >> transform_load_weather_data

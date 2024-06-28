# Building an Efficient ETL Pipeline with Weather map API


##  Project Overview
This project demonstrates a data pipeline that extracts weather data from an API, transforms it, and loads it into an S3 bucket using Apache Airflow. The pipeline ensures the API's availability before extracting the data, transforms the data into a structured format, and stores it in a CSV file on AWS S3.

## Table of Content
1. Project Scope and Objectives
2. Technologies Used
3. Setup Instructions
4. Pipeline Description
5. Code Explanation
6. Usage
7. Contributing
8. License

## Project Scope and Objectives

### Scope
The scope of this project is to develop an ETL (Extract, Transform, Load) pipeline that automates the process of fetching, processing, and storing weather data in cloud storage.
### Objectives
- Verify the availability of the weather API.
- Extract weather data for a specific location.
- Transform the extracted data into a readable format.
- Load the transformed data into an S3 bucket.

## Technology Used
- Apache Airflow: Workflow management
- Docker: Containerization
- Python: Programming language
- Pandas: Data manipulation
- AWS S3: Cloud storage

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed on your machine
- AWS account with S3 bucket and IAM user with proper permissions
- API key for the weather API

### Steps
1. Clone the repository:
```bash
git clone https://github.com/philtee1/weather-api-etl-pipeline.git
cd weather-api-etl-pipeline
```

2. Install required libraries using `pip install <library_name>` (e.g. pandas, boto3). Required dependencies stored in `requirement.txt`

3. Configure Airflow connections:
`weathermap_api`: Connection to the weather API with endpoint URL and authentication.

4. Set environment variables for AWS S3 credentials (AccessKeyId, SecretAccessKey, SessionToken)

5. Create a `.env` file and add your AWS credentials and API key:
```plaintext
AccessKeyId=YOUR_AWS_ACCESS_KEY_ID
SecretAccessKey=YOUR_AWS_SECRET_ACCESS_KEY
SessionToken=YOUR_AWS_SESSION_TOKEN
WEATHER_API_KEY=YOUR_WEATHER_API_KEY
```

6. Build and run the Docker containers:
```bash
docker-compose up -d
```

7. Access the Airflow web interface at `http://localhost:8080` and trigger the DAG named weather_dag.

## Pipeline Description
- API Availability Check: Ensures the weather API is available using `HttpSensor`.
- Data Extraction: Fetches weather data using `SimpleHttpOperator`.
- Data Transformation and Loading: Processes the data and saves it to an S3 bucket using a `PythonOperator`.

## Code Explanation

### DAG Definition
The DAG consists of three primary tasks:

1. weather_api_readiness:
Uses an HttpSensor to confirm the weather API is available before proceeding.

2. extract_weather_data:
Retrieves weather data for Portland using a SimpleHttpOperator. The response is converted to JSON format.

3. transform_load_weather_data:
Uses a PythonOperator to transform the extracted data (e.g., converts Kelvin to Fahrenheit, formats timestamps) and loads it into a CSV file in an S3 bucket.

## Usage
- Start the pipeline by accessing the Airflow UI and triggering the DAG.
- Monitor the pipeline's progress in the Airflow UI.
- Verify the data is saved correctly in your S3 bucket.

## Contributing 
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License
This project is licensed under the MIT License.




"# ETL_Pipeline_Weather_Map" 
"# ETL_Pipeline_Weather_Map" 
"# ETL_Pipeline_Weather_Map" 

import os 
import csv
from django.conf import settings
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherData:
    date: datetime
    max_temperature: float
    min_temperature: float
    max_humidity: int
    min_humidity: int
    mean_humidity: int

    colum_mapping={
        "Max TemperatureC": "max_temperature",
        "Min TemperatureC": "min_temperature",
        "Max Humidity": "max_humidity",
        "Min Humidity": "min_humidity",
        "Mean Humidity": "mean_humidity",
    } 
   

    def __post_init__(self):
        self.date = datetime.strptime(self.date, "%Y-%m-%d")
        self.max_temperature = float(self.max_temperature)
        self.min_temperature = float(self.min_temperature)
        self.max_humidity = int(self.max_humidity)
        self.min_humidity = int(self.min_humidity)
        self.mean_humidity = int(self.mean_humidity)
    
class Fileparser:
    def __init__(self, path="\weather_app\data"):
          self.dir_path=str(settings.BASE_DIR) + path

    def get_files_by_year(self,year):
    # Retrieve all files that match the given year.
           year_files = []
           
           for file in os.listdir(self.dir_path):
            if str(year) in file and file.endswith(".txt"):
              year_files.append(os.path.join(self.dir_path, file)) 
           return year_files
    
    def get_file_data(self, to_read, required_columns):
        # Store extracted rows
        extracted_data = []
        with open(to_read, 'r') as file:
            reader = csv.reader(file)
            header_row = next(reader)
            headers = [column.strip() for column in header_row]
            column_indices = {col:headers.index(col) for col in required_columns if col in headers}
            for row in reader:
                try:
                    extracted_data.append(
                        WeatherData(
                            date=row[column_indices["PKT"] ],
                            max_temperature=row[column_indices["Max TemperatureC"]],
                            min_temperature=row[column_indices["Min TemperatureC"]],
                            max_humidity=row[column_indices["Max Humidity"]],
                            min_humidity=row[column_indices["Min Humidity"]],
                            mean_humidity=row[column_indices["Mean Humidity"]]
                        )
                    )
                except ValueError:
                    print(f"Skipping invalid row: {row}")

        return extracted_data
          
    def formatdata(self, extracted_data):
        formatted_result = []
        
        for data in extracted_data:  
            if hasattr(data, "Max_temperature"):  # Ensure it has the attribute
                formatted_result.append(
                    f"Max Temp: {data.Max_temperature}°C, \n"
                    f"Min Temp: {data.Min_temperature}°C, \n"
                    f"Max Humidity: {data.Max_Humidity}%"
                    f"min humidity:{data.min_humidity}%"
                )
            else:
                print("Warning: Data object does not have expected attributes", data)

        return "\n".join(formatted_result)

class Calculation:
    def __init__(self, extracted_data):
        self.extracted_data = extracted_data
    def get_max_temperature(self):
        max_temp=None
        max_date=None

        for data in self.extracted_data:
            if isinstance(data.max_temperature,(int, float)):
                if max_temp is None or data.max_temperature > max_temp:
                 max_temp = data.max_temperature
                 max_date = data.date

        if max_temp is None:
            return "No valid temperature data found"

        return f"Minimum Temperature: {max_temp}°C on {max_date.strftime('%Y-%m-%d')}"        

    def get_min_temperature(self):
        min_temp = None 
        min_date = None
        
        for data in self.extracted_data:
            if isinstance(data.min_temperature, (int, float)): 
                if min_temp is None or data.min_temperature < min_temp: 
                    min_temp = data.min_temperature
                    min_date = data.date 

        if min_temp is None:
            return "No valid temperature data found"

        return f"Minimum Temperature: {min_temp}°C on {min_date.strftime('%Y-%m-%d')}"
    
    def get_max_huimidity(self):
        max_humid=None
        max_hum_date=None
        for data in self.extracted_data:
            if(isinstance(data.max_humidity,(int,float))):
                if max_humid is None or data.max_humidity >max_humid:
                    max_humid= data.max_humidity
                    max_hum_date = data.date
            
        if max_humid is None:
            return "No valid Humidity  data found"  
        
        return f"Max humidity: { max_humid} % on {max_hum_date.strftime('%Y-%m-%d')}"

    def get_min_huimidity(self):
        min_humid=None
        min_humid_date=None

        for data in self.extracted_data:
            if isinstance(data.min_humidity, (int,float)):
                if min_humid is None or data.min_humidity < min_humid:
                    min_humid = data.min_humidity
                    min_humid_date = data.date

        if min_humid is None:
            return "no valid data found"
            
        return f"Min humidity: {min_humid} % on {min_humid_date.strftime('%Y-%m-%d')}"

    def average_max_temperature(self,year,month):
      
         max_temperatures = [data.max_temperature for data in self.extracted_data 
                            if data.date.year == year and data.date.month == month]

         if not max_temperatures:
            return "No data available for the given month"

         return round(sum(max_temperatures) / len(max_temperatures), 2)
        
    def average_min_temp(self,year,month):
            min_temperature=[data.min_temperature for data in self.extracted_data 
                             if data.date.year == year and data.date.month ==month
                            ]
            if not min_temperature:
                return "no data avalible"
            return round(sum(min_temperature)/ len(min_temperature),2)

    def average_mean_humidity(self,year,month):
            average_mean=[data.mean_humidity for data in self.extracted_data
                       if data.date.year == year and data.date.month == month
                    ]
            if not average_mean: 
                return "no data avalible"
            return round(sum(average_mean)/len(average_mean),2)
    
    def bar_chart(self, average_max, average_min):
        # Ensure values are integers before multiplying
        if not isinstance(average_max, int) or not isinstance(average_min, int):
            raise TypeError("average_max and average_min must be integers")
        print(f"Avg Max Temperature ({average_max}°C): {'*' * average_max}")
        print(f"Avg Min Temperature ({average_min}°C): {'*' * average_min}")





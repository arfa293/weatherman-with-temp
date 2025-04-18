import os
import csv
from django.core.management.base import BaseCommand
from weather_app.models import WeatherRecord  

class Command(BaseCommand):
    help = "Import all CSV files into a single WeatherRecord table"

    def handle(self, *args, **kwargs):
        folder_path = os.path.abspath("weather_app/data")  
        input_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".txt")]

        if not input_files:
            self.stdout.write(self.style.ERROR("No CSV files found in 'weather_app/data'"))
            return

        for file_path in input_files:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)  

                for row in reader:
                    try:
                        WeatherRecord.objects.create(
                             date=row[0] if row[0] else None, 
                             max_Temperature=float(row[1]) if row[1] else None,
                             min_Temperature=float(row[3]) if row[3] else None,
                             humidity=int(row[8]) if row[8] else None, 
                             max_Humidity=int(row[7]) if row[7] else None,
                            min_humidity=int(row[9]) if row[9] else None,
                                )
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Skipping row due to error: {e}"))

        self.stdout.write(self.style.SUCCESS("All CSV data successfully imported into WeatherRecord table!"))

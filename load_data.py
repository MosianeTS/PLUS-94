import os
import django
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') 

django.setup()

from students.models import Candidate

csv_file_path = 'C:\\Users\\mosia\\OneDrive\\Desktop\\Refresh\\project_data.csv'  

with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file, delimiter=';', fieldnames=['candidate', 'score', 'scoring_date', 'province'])
    next(reader)  

    for row in reader:
        print(f"Processing row: {row}")  
        try:
            candidate = Candidate(
                candidate=row['candidate'].strip(),
                score=int(row['score'].strip()),
                scoring_date=datetime.strptime(row['scoring_date'].strip(), '%Y/%m/%d').date(),
                province=row['province'].strip()
            )
            candidate.save()
        except Exception as e:
            print(f"Error processing row {row}: {e}")


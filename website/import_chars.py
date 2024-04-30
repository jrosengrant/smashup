import os, django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()
from chars.models import Character 

def import_books(file_path):
    Character.objects.all().delete()

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            # walljump = True if "TRUE" else False
            Character.objects.get_or_create(
                char_name = row['Full Name'],
                weight = row['Weight'],
                num_jumps = row['Number of Jumps'],
                max_run_vel = row['Run Maximum Velocity'],
                jump_height = row['Jump Heights'],
                hop_height = row['Hop Heights'],
                air_jump_height = row['Air Jump Heights'],
                max_h_air_speed = row['Maximum Horizontal Air Speed'],
                fastfall_speed = row['Fastfall Speed'],
                has_walljump = True if "TRUE" else False
            )
            print(Character.objects.filter(char_name=row['Full Name']))

if __name__ == '__main__':
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', "ult_params.csv")
    print(csv_file_path)  
    import_books(csv_file_path)
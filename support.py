import csv
import ast
import json 

def convert_dictionary(element):
    element['Id'] = int(element['Id'])
    element['Duration'] = int(element['Duration'])
    element['CalcPrio'] = int(element['CalcPrio'])
    element['LastResults'] = ast.literal_eval( element['LastResults'] )
    element['Verdict'] = int(element['Verdict'])
    element['Cycle'] = int(element['Cycle'])
    element['Depend'] = []

def get_dataset(file_name: str) -> dict:
    dataset = {}
    with open(file_name, newline="\n") as csvfile:
        reader = csv.DictReader(csvfile,  delimiter=';')
        for row in reader:
            convert_dictionary(row)
            dataset[row['Id']] = row
    return dataset


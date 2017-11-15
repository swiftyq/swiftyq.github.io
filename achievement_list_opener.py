import csv
import json

def returner():
    csvfile = open('static/achievement/achievement_list.csv')

    fieldname = ("num", "title", "content")
    reader = csv.DictReader(csvfile, fieldname)
    out = json.dumps([row for row in reader])
    return out

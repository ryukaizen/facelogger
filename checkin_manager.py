import requests
from datetime import datetime

class CheckinManager:
    def __init__(self, google_form_url, entry_name_id, entry_time_id):
        self.google_form_url = google_form_url
        self.entry_name_id = entry_name_id
        self.entry_time_id = entry_time_id
        self.checkin_dict = {}

    def mark_checkin(self, name):
        if name not in self.checkin_dict:
            self.checkin_dict[name] = True
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            form_data = {
                self.entry_name_id: name,
                self.entry_time_id: current_time,
            }
            requests.post(self.google_form_url, data=form_data)
    
    def mark_checkin_csv(name):
        with open('facelogs/facelogs.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
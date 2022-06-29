import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from copy import deepcopy

CREDENTIALS_FILE = 'creds.json'

with open('spread.txt') as s:
    spreadsheet_id = s.read()

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

class Schedule():
    def __init__(self):
        self.days = [
            ['monday1', 'C2:D6', []],
            ['tuesday1', 'C8:D12', []],
            ['wednesday1', 'C14:D18', []],
            ['thursday1', 'C20:D24', []],
            ['friday1', 'C26:D30', []],
            ['saturday1', 'C32:D36', []],
            ['monday2', 'F2:G6', []],
            ['tuesday2', 'F8:G12', []],
            ['wednesday2', 'F14:G18', []],
            ['thursday2', 'F20:G24', []],
            ['friday2', 'F26:G30', []],
            ['saturday2', 'F32:G36', []],
        ]
        self.prevSchedule = deepcopy(self.days)
        self.currentWeek = None
        self.updateDays = set()
        self.isFirstLaunch = True
    
    def setCurrentWeek(self):
        values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='C1',
                majorDimension='ROWS'
            ).execute()
        self.currentWeek = values['values'][0][0]

    def setPrevSchedule(self):
        self.prevSchedule = deepcopy(self.days)

    def setSchedule(self, values):
        for i in range(len(self.days)):
            self.days[i][2] = values[i]

    def readingSheets(self):
        schedule = []
        for day in self.days:
            values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=day[1],
                majorDimension='ROWS'
            ).execute()
            try:
                schedule.append(values['values'])
            except:
                schedule.append([])

        self.setPrevSchedule()
        self.setSchedule(schedule)

    def checkNewWeek(self):
        values = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='C1',
                majorDimension='ROWS'
            ).execute()
        return self.currentWeek != values['values'][0][0]

    def checkUpdate(self):
        if self.prevSchedule != self.days:
            if self.checkNewWeek():
                for i in range(6):
                    if self.prevSchedule[i+6][2] != self.days[i][2]:
                        self.updateDays.add(i)
            else:
                for i in range(len(self.days)):
                    if self.days[i] != self.prevSchedule[i]:
                        self.updateDays.add(i)
        self.setCurrentWeek()
        return self.updateDays

    def resetToZeroUpdateDays(self):
        self.updateDays = set()
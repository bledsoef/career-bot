import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd


class Spreadsheet:
    def __init__(self, data):
        self.data = data
    
    def setup_sheet(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file('bc-career-bot-00e3f146da3a.json', scopes=scopes)

        gc = gspread.authorize(credentials)

        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        # open a google sheet
        self.gs = gc.open_by_key('1sZUo62mCo4vMAYBJCwVlIHOCYmsfRzAj6vctUMqaeYo')
        # select a work sheet from its name
        self.worksheet_main = self.gs.worksheet('Main')

    def append(self):
        # dataframe (create or import it)
        print(self.data)
        df = pd.DataFrame(self.data)
        df_values = df.values.tolist()
        self.gs.values_append('Main', {'valueInputOption': 'RAW'}, {'values': df_values})
    
    def run(self):
        self.setup_sheet()
        self.append()
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Spreadsheet
SCOPE_GOOGLE_SPREAD_SHEET = [
  "https://www.googleapis.com/auth/spreadsheets.readonly"
]

# Path
path_service_account = os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/credentials/service-account.json")
scopes = SCOPE_GOOGLE_SPREAD_SHEET

def _build_service():
  # Authenticate with the service account and build the API client
  with open(path_service_account) as json_file:
    json_data = json.load(json_file)
    creds = service_account.Credentials.from_service_account_info(json_data, scopes=SCOPE_GOOGLE_SPREAD_SHEET)
  return build('sheets', 'v4', credentials=creds)

def _read_spreadsheet(service, spreadsheetId, worksheetName):
  # Read the specific sheet
  result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetId,
    range=worksheetName
  ).execute()
  
  # Read data
  rows = result.get('values', [])
  return rows[1:]

def get_values_spreadsheet(spread_sheet_id, work_sheet_name):
  # init
  service = _build_service()
  
  # Meta data
  rows = _read_spreadsheet(service, spread_sheet_id, work_sheet_name)

  return rows
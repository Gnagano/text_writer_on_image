import os, glob
import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Spreadsheet
# SPREAD_SHEET_ID = os.environ['SPREAD_SHEET_ID']
SPREAD_SHEET_ID = "1_JLcC6-qbHB1y0CbcaToeQRKk0n5mttu0T-xVZc8mkc"
WORK_SHEET_ARTICLE_NAME = "articles"
# WORK_SHEET_META_NAME = os.environ['SPREAD_SHEET_WORK_SHEET_META_NAME']
SCOPE_GOOGLE_SPREAD_SHEET = [
  "https://www.googleapis.com/auth/spreadsheets.readonly"
]
# PATH_SERVICE_ACCOUNT = os.environ['SPREAD_SHEET_CREDENTIALS_FILE_GUEST']
# SHEET_NAME_TEMPLATE = os.environ['SPREAD_SHEET_SHEET_NAME_TEMPLATE']
# SHEET_NAME_ARTICLES = os.environ['SPREAD_SHEET_SHEET_NAME_ARTICLE']
# SHEET_NAME_BLOG = os.environ['SPREAD_SHEET_SHEET_NAME_BLOG']

# Wordpress
# DIR_ARTICLES = os.environ['WP_POST_DIR_GUEST']
# DIR_META = os.environ['WP_META_DIR_GUEST']
# DIR_BLOG = os.environ['WP_BLOG_DIR_GUEST']
# TEMPLATE_MESSAGE = os.environ['WP_TEMPLATE_H4_MESSAGE']
# DIR_BLOG = os.environ['WP_BLOG_DIR_GUEST']
# TEMPLATE_MESSAGE = os.environ['WP_TEMPLATE_H4_MESSAGE']


# Path
path_service_account = os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/credentials/service-account.json")
scopes = SCOPE_GOOGLE_SPREAD_SHEET

def build_service():
  # Authenticate with the service account and build the API client
  with open(path_service_account) as json_file:
    json_data = json.load(json_file)
    creds = service_account.Credentials.from_service_account_info(json_data, scopes=scopes)
  return build('sheets', 'v4', credentials=creds)

def read_spreadsheet(service, spreadsheetId, worksheetName):
  # Read the specific sheet
  result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetId,
    range=worksheetName
  ).execute()
  
  # Read data
  rows = result.get('values', [])
  return rows

def get_metadata (rows):
  return {
    'title': rows[0][1],
    'description': rows[1][1],
  }   

def get_article (rows):
  # Read only rows of the articles
  articles_with_label = []
  found_articles = False
  for row in rows:
      if found_articles:
          articles_with_label.append(row)
      elif len(row) > 0 and row[0] == 'title':
          found_articles = True
  
  return articles_with_label

# def split_metadata_and_articles (rows):
#   meta = {
#     'title': rows[0][1],
#     'description': rows[1][1]
#   };
  
#   # Read only rows of the articles
#   articles_with_label = []
#   found_articles = False
#   for row in rows:
#       if found_articles:
#           articles_with_label.append(row)
#       elif len(row) > 0 and row[0] == 'articles':
#           found_articles = True
  
#   # Remove the row of label
#   articles = articles_with_label[1:]
#   return { 'metadata': meta , 'articles': articles }

def export_articles(articles):
  # Write articles
  for index, article in enumerate(articles, start=1):
    title = article[0]
    tag = article[2]

    # Remove useless header
    parts = article[1].split('<h2>プリフェース</h2>', 1)
    content_with_hashes = parts[1] if len(parts) > 1 else ''
    content = re.sub(r'^#+', '', content_with_hashes, flags=re.MULTILINE)
    
    serial_number = "00" + str(index) if index < 10 else "0" + str(index)
    serial_number = serial_number[-3:]
    with open(f"{DIR_ARTICLES}/article{serial_number}.txt", "w") as f:
      f.write(f"{title}\n{tag}\n{content}\n")

def export_metadata(metadata):
  with open(f"{DIR_META}/meta.txt", "w") as f:
    f.write(f"{metadata['title']}\n{metadata['description']}\n")

# def create_post_template(service): 
#   # Read Template
#   result = service.spreadsheets().values().get(
#     spreadsheetId=SPREAD_SHEETS_ID,
#     range=SHEET_NAME
#   ).execute()
#   rows = result.get('values', [])
  
#   # Write Template
#   with open(f"{DIR_BLOG}/template.php", 'w') as f:
#     f.write(f"<h4>{TEMPLATE_MESSAGE}</h4>" + '\n')
#     for row in rows[1:]:
#       link = row[0]
#       img_url = row[1]
#       width = row[2] if len(row) > 3 else ''
#       height = row[3] if len(row) > 4 else ''
      
#       img_tag = '<img decoding="async" src="{}" alt="" width="{}" height="{}" border="0" />'.format(img_url, width, height)
#       a_tag = '<a href="{}" rel="nofollow">{}</a>'.format(link, img_tag)
#       p_tag = '<p>{}</p>'.format(a_tag)
      
#       f.write(p_tag + '\n')

def main():
  # init
  service = build_service()
  
  # Meta data
  rows = read_spreadsheet(service, SPREAD_SHEET_ID, WORK_SHEET_ARTICLE_NAME)
  print(rows)
  # metadata = get_metadata(rows_meta)
  # print(metadata)
  
  # Articles
  # rows_article = read_spreadsheet(service, SPREAD_SHEET_ID, WORK_SHEET_ARTICLE_NAME)
  # articles = get_article(rows_article)
  
  # Export (Metadata and Articles)
  # export_articles(articles)
  # export_metadata(metadata)

if __name__ == '__main__':
  main()

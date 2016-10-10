import requests
import sys
import pprint
import json

url = 'https://api.discogs.com/users/{0}/collection/folders/0/releases?page={1}'
pp = pprint.PrettyPrinter()

def get_collection(username):
  collection = set();
  pages = 1
  current_page = 0
  while current_page < pages:
    r = requests.get(url.format(username, current_page) , headers=headers)
    
    if r.status_code == 200:
      j = json.loads(r.text)
      
      pages = j["pagination"]["pages"]
      current_page += 1
      
      for release in j["releases"]:
        collection.add(release["basic_information"]["title"])
        
  return collection
  
def compare_collections(username1, username2):
  collection1 = get_collection(username1)
  collection2 = get_collection(username2)
  
  result = collection1.intersection(collection2)
  pp.pprint(result)

if len(sys.argv) > 1 and sys.argv[1] == '--help':
  print ("Usage: compare.py username1 username2")
  sys.exit()

if len(sys.argv) != 3:
  print ("Wrong arguments supplied, use --help to see arguments")
  sys.exit()
 
user1 = sys.argv[1]
user2 = sys.argv[2]

if user1.lower() == user2.lower():
  print ("The two users are the same")
  sys.exit()

headers = {
  'User-Agent': 'CompareUsers/0.1'
}
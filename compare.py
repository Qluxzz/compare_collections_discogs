import requests
import sys
import pprint
import json
import time
from operator import itemgetter

url = 'https://api.discogs.com/users/{0}/collection/folders/0/releases?page={1}'

pp = pprint.PrettyPrinter()

headers = {
  'User-Agent': 'CompareUsers/0.1'
}

def print_incremental(text):
  sys.stdout.write('Releases: {0}\r'.format(text))
  sys.stdout.flush()

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
        info = release["basic_information"]
        title = info["title"]
        artist = info["artists"][0]["name"]
        collection.add((artist, title))
        print_incremental(len(collection))
    time.sleep(0.25)
  print_incremental(len(collection))
  print("")
  return collection

def get_longest_artist_name(results):
  current_longest = 0
  for result in results:
    if len(result[0]) > current_longest:
      current_longest = len(result[0])
  return current_longest

def print_results(results, username1, username2):
  if len(results) == 0:
    print ("No releases in common")
    return
  print ("Releases in common between {0} and {1}: {2}".format(username1, username2, len(results)))
  longest_artist = get_longest_artist_name(results)
  print ("Artist", end="")
  for x in range(len("Artist"), longest_artist):
     print("-", end="")
  print("|Album")
  for result in results:
   length = len(result[0])
   print (result[0], end="")
   for x in range(length, longest_artist):
     print (" ", end="")
   print ("|", end="")
   print (result[1])

def compare_collections(username1, username2):
  print ("Getting {0}'s collection".format(username1))
  collection1 = get_collection(username1)
  print ("Getting {0}'s collection".format(username2))
  collection2 = get_collection(username2)
  print ("Comparing collections")
  result = collection1.intersection(collection2)
  print_results(result, username1, username2)


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

compare_collections(user1, user2)

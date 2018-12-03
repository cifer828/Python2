"""
get POIs of Shanghai using weibo check-in data
author: Cifer Zhang
"""
from weibo import APIClient
import webbrowser
import json
import sqlite3
import urllib

APP_KEY = "3708656745"      # app key
APP_SECRET = "8c667da0f518a0695fc9b69f1ceb7eb2"     # app secret
CALLBACK_URL = "http://open.weibo.com/apps/3708656745/info/advanced"       # callback url

def connection2api():
    """
    get access token using webibo API
    return an available client
    """
    # retrieve token
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    webbrowser.open_new(url)    # click auth in browser
    # input strings after 'code=' in the url of newly opened page
    code = raw_input("input the code: ")
    r = client.request_access_token(code)
    access_token = r.access_token   # weibo token
    expires_in = r.expires_in   # token expiration
    client.set_access_token(access_token, expires_in)   # save token\
    return client

def auto_login():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    web_conn = urllib.urlopen(url)
    print web_conn.info()
    print web_conn.read()

def save_one_page(conn, client, page):
    one_page_json = client.place.nearby.pois.get(lat= 31.241280, long=121.321815, range = 10000, count = 50, sort = 1, page = page)
    cur = conn.cursor()
    # create table
    cur.execute('''CREATE TABLE IF NOT EXISTS pois (title TEXT, lat FLOAT, checkin INTEGER, lon FLOAT, category_name TEXT,
                   district_name TEXT, PRIMARY KEY (title))''')
    for poi in one_page_json["pois"]:
        title = poi['title']
        lat = poi['lat']
        lon = poi['lon']
        category = poi['category']
        category_name = poi['category_name']
        district_id = poi['district']
        district_name = poi['district_name']
        check_ins = poi['checkin_num']

        # print title, lat, lon, category, check_ins
        cur.execute('SELECT title FROM pois WHERE title = ? LIMIT 1', (title, ) )
        try:
            count = cur.fetchone()[0]
        except:
            cur.execute('INSERT INTO pois (title, lat, lon, checkin, category_name, district_name) VALUES (?, ?, ?, ?, ? ,?)',
                        (title, lat, lon, check_ins, category_name, district_name) )
        #     cur.execute('''UPDATE Weibo_pois SET title = ?, lat = ?, lon = ?, category = ?,  WHERE title = ?''',
        #                 (title, lat, lon, category, title) )
    conn.commit()
    cur.close()
    return json.dumps(one_page_json, ensure_ascii=False, indent=4)

def save_pois():
    # print json.dumps(one_page_json, ensure_ascii=False, indent=4)
    client = connection2api()
    conn = sqlite3.connect('weibo_pois.sqlite')     # new database
    page = 21
    while(True):
        # print json.dumps(one_page_json, ensure_ascii=False, indent=4)     # print one page result
        save_one_page(conn, client, page)
        print "page %d saved" % page
        page += 1

def rate_limit():
    client = connection2api()
    return json.dumps(client.account.rate_limit_status.get(), indent=4)

# print rate_limit()
save_pois()
# print save_one_page(sqlite3.connect('weibo_pois.sqlite') , connection2api(), 1)

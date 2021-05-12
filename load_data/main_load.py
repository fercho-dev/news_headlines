import argparse
import psycopg2
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd

logger = logging.getLogger(__name__)

def connect_to_db():
    ## connect to the db
    host = ""
    db = ""
    user = ""
    pw = ""

    conn = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = pw)
    cur = conn.cursor()
    return conn

def create_cursor(conn):
    cur = conn.cursor()
    return cur

def main(filename):
    conn = connect_to_db()
    cur = create_cursor(conn)
    headlines = pd.read_csv(filename)

    for index, row in headlines.iterrows():
        #logger.info('loading headline id {} into db').format(row['id'])
        headline = row['headline']
        news_site = row['news_site']
        news_section = row['news_section']
        date = row['date']
        link = row['link']
        host = row['host']

        cur.execute ('''
        INSERT INTO headlines ("headline", "news site", "news section", "date", "link", "host") 
        VALUES (%s, %s, %s, %s, %s, %s);
        ''', (headline, news_site, news_section, date, link, host,))
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info('data inserted to database')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='the file you want to load into the db',
                        type=str)
    args = parser.parse_args()
    main(args.filename)

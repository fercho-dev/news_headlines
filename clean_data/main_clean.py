import argparse
import hashlib
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse
import datetime
import os
import pandas as pd 

logger = logging .getLogger(__name__)

def main(filename):
    logger.info('starting cleaning process')

    df = _read_data(filename)
    df = _extract_host(df)
    df = _drop_duplicates(df)
    df = _drop_rows_with_missing_data(df)
    df = _generate_ids_for_headlines(df)
    _save_data(df, filename)

    return df


def _read_data(filename):
    logger.info('reading files {}'.format(filename))
    return pd.read_csv(filename)

def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['link'].apply(lambda link:urlparse(link).netloc)
    return df

def _drop_duplicates(df):
    logger.info('removing duplicate entries')
    df.drop_duplicates(subset=['headline'], keep='first', inplace=True)
    return df

def _drop_rows_with_missing_data(df):
    logger.info('dropping rows with mising values')
    return df.dropna()

def _generate_ids_for_headlines(df):
    logger.info('generating ids for each row')
    ids = (df
           .apply(lambda row: hashlib.md5(bytes(row['link'].encode())), axis=1)
           .apply(lambda hash_object: hash_object.hexdigest())
          )
    
    df['id'] = ids

    return df.set_index('id')
    
def _save_data(df, filename):
    #now = datetime.datetime.now().strftime('%Y/%m/%d')
    clean_filename = 'clean_headlines.csv'
    logger.info('saving data at location: {}'.format(clean_filename))
    df.to_csv(clean_filename, encoding='utf-8')
    os.remove(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='the path to the data',
                        type=str)
    
    args = parser.parse_args()

    df = main(args.filename)
import argparse
import logging
logging.basicConfig(level=logging.INFO)
import subprocess

logger = logging.getLogger(__name__)


def main(news_site_uid):
    _extract(news_site_uid)
    _transform()
    _load()

def _extract(news_site_uid):
    logger.info('starting extraction process')
    subprocess.run(['python3.7', 'main_get.py', news_site_uid], cwd='./get_data')
    subprocess.run(['mv', 'headlines.csv', '../clean_data'], cwd='./get_data')

def _transform():
    logger.info('starting cleaning process')
    dirty_data = 'headlines.csv'
    clean_data = 'clean_headlines.csv'
    subprocess.run(['python3.7', 'main_clean.py', dirty_data], cwd='./clean_data')
    subprocess.run(['mv', clean_data, '../load_data'], cwd='./clean_data')

def _load():
    logger.info('starting load process')
    clean_data = 'clean_headlines.csv'
    subprocess.run(['python3.7', 'main_load.py', clean_data], cwd='./load_data')
    subprocess.run(['rm', clean_data], cwd='./load_data')



if __name__ == '__main__':
    news_site_choices = ['elpais', 'eluniversal']
    parser = argparse.ArgumentParser()
    parser.add_argument('news_site',
                        help='the news site you want to scrape',
                        type=str,
                        choices=news_site_choices)
    args = parser.parse_args()
    main(args.news_site)
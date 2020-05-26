import argparse
import datetime
import csv
import logging
logging.basicConfig(level=logging.INFO)
import news_page_objects as news
from common import config
import re

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _news_scraper(news_site_uid, news_section_uid):
    host = config()['news_sites'][news_site_uid]['queries'][news_section_uid]['url']
    logging.info('beginning scraper for {}'.format(host))
    headlines = _fetch_headlines(news_site_uid, news_section_uid, host)
    #for headline in headlines:
        #print('{}\n{}\n\n'.format(headline[0],headline[1]))
    
    _save_headlines(news_site_uid, news_section_uid, headlines)

def _save_headlines(news_site_uid, news_section_uid, headlines):
    now = datetime.datetime.now().strftime('%Y/%m/%d')
    out_file_name = 'headlines.csv'
    with open(out_file_name, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow(['headline','news_site','news_section', 'date', 'link'])

        for headline in headlines:
            #row = [str(getattr(headline, prop)) for prop in csv_headers]
            row = [headline[0], news_site_uid, news_section_uid, now, headline[1]]
            writer.writerow(row)


def _fetch_headlines(news_site_uid, news_section_uid, host):
    logger.info('Start fetching at {}'.format(host))
    if news_site_uid == 'elpais':
        headlines = _fetch_headlines_elpais(news_site_uid, news_section_uid, host)
    elif news_site_uid == 'eluniversal':
        headlines = _fetch_headlines_eluniversal(news_site_uid, news_section_uid, host)
    else:
        pass

    return headlines

def _fetch_headlines_eluniversal(news_site_uid, news_section_uid, host):
    section_page = news.SectionPage(news_site_uid, news_section_uid, host)

    headlines1 = section_page._html.find_all('h1', attrs={'class':'field-content'})
    headlines_list1 = [[result.get_text(), result.find('a').get('href')] for result in headlines1]
    for item in headlines_list1:
        tmp = _build_link(news_site_uid, news_section_uid, host, item[1])
        item[1] = tmp

    headlines2 = section_page._html.find_all('h2', attrs={'class':'field-content'})
    headlines_list2 = [[result.get_text(), result.find('a').get('href')] for result in headlines2]
    for item in headlines_list2:
        tmp = _build_link(news_site_uid, news_section_uid, host, item[1])
        item[1] = tmp

    headlines_list = headlines_list1 + headlines_list2
    
    return headlines_list

def _fetch_headlines_elpais(news_site_uid, news_section_uid, host):
    section_page = news.SectionPage(news_site_uid, news_section_uid, host)
    headlines = section_page._html.find_all('h2', attrs={'class':'headline'})
    headlines_list = [[result.get_text(), result.find('a').get('href')] for result in headlines]
    for item in headlines_list:
        tmp = _build_link(news_site_uid, news_section_uid, host, item[1])
        item[1] = tmp
    
    return headlines_list

def _build_link(news_site_uid, news_section_uid, host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        if news_site_uid == 'elpais':   
            host = host.rstrip('/').rstrip(news_section_uid).rstrip('/')
            return '{}{}'.format(host, link)
        else:
            return '{}{}'.format(host, link)
    else:
        if news_site_uid == 'elpais':
            link = link.rstrip('/america/')
            return '{host}/{uri}'.format(host=host, uri=link)
        else:
            return '{host}/{uri}'.format(host=host, uri=link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='the news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    news_section_choices = list(config()['news_sites'][args.news_site]['queries'].keys())
    news_section_uid = input('choose a section: {}\n'.format(news_section_choices))
    _news_scraper(args.news_site, news_section_uid)

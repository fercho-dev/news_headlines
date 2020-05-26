from common import config
import requests
from bs4 import BeautifulSoup

class NewsPage:

    def __init__(self, news_site_uid, news_section_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)
    
    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()

        self._html = BeautifulSoup(response.text, 'html.parser')

#class HomePage(NewsPage):

    #def __init__(self, news_site_uid, url):
        #super().__init__(news_site_uid, url)

    #@property
    #def sections(self):
        #section_list = []
        #for section in self._select(self._queries['home_page_sections']):
            #if section and section.has_attr('href'):
                #section_list.append(section)
        
        #return [[section.get_text(), section.get('href')] for section in section_list]

class SectionPage(NewsPage):

    def __init__(self, news_site_uid, news_section_uid, url):
        super().__init__(news_site_uid, news_section_uid, url)

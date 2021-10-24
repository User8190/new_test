import requests
import urllib
from requests_html import HTMLSession

def search():
    def sites():
        site_list = ['baiscopelk.com', 'cineru.lk', 'piratelk.com']
        output = " "
        for i in site_list:
            output = output+"site:"+str(i)+" "
            if i != site_list[len(site_list)-1]:
                output = output+"OR "
        output = output+'1..10'
        return output


    def get_source(url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)


    def scrape_google(query):
        query = query + sites()
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.uk/search?q=" + query)

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.',
                          'https://google.',
                          'https://webcache.googleusercontent.',
                          'http://webcache.googleusercontent.',
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links


    def get_results(query):
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.uk/search?q=" + query)
        return response


    def parse_results(response):
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".IsZvec"
        results = response.html.find(css_identifier_result)
        title = []
        link = []
        description = []
        for result in results:
            title.append(result.find(css_identifier_title, first=True).text)
            link.append(result.find(css_identifier_link, first=True).attrs['href'])
            description.append(result.find(css_identifier_text, first=True).text)

        output = {"title": title, 'link': link, "description": description}

        return output


    def google_search(query):
        query = query + sites()
        response = get_results(query)
        return parse_results(response)


def search_engine(query):
    try:
        dic = google_search(query)
        links = dic['link']
        titles = dic['title']
        link_list = []
        title_list = []
        for i in range(len(links)):
            site_list = ["https://cineru.lk/", "https://www.baiscopelk.com/", "https://piratelk.com/"]
            link = links[i]
            for j in site_list:
                link = link.replace(j, "")
            if link.count('/') == 1:
                link_list.append(links[i])
                title_list.append(titles[i])
                print(link.count('/'))
        output = {"link":link_list, 'title':title_list}
        return output
    except Exception as e:
        return "Not Result"

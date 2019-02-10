import urllib3
import certifi
import lxml
from bs4 import BeautifulSoup as BS
from lxml.html.clean import Cleaner

doc_id = 0


def find_all_links(html):
    soup = BS(html, features="lxml")
    output = []
    for link in soup.find_all('a'):
        if not output.count(link.get('href')) > 0 and link.get('href') is not None:
            if link.get('href').startswith('/'):
                output.append(base_url + link.get('href'))
            else:
                output.append(link.get('href'))
    return output


def strip_tags(web_content):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True

    text = BS(lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(web_content))), features="lxml")
    return text.getText()


def get_raw_html(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    r = http.request('GET', url)
    web_content = r.data.decode('utf8')
    return web_content


def iterate_links(links_list, page_content):
    global doc_id
    for l in links_list:
        if l.startswith('http') and l not in visited_urls:
            f = open(str(doc_id) + '.txt', 'w', encoding="utf-8")
            output_text = strip_tags(page_content)
            f.write(output_text)
            f.close()
            visited_urls.add(l)
            doc_id += 1
            new_page_content = get_raw_html(l)
            new_list = find_all_links(page_content)
            if len(visited_urls) < 200:
                iterate_links(new_list, new_page_content)


base_url = 'https://flutter.io'
visited_urls = {"", }

content = get_raw_html(base_url)
out = find_all_links(content)
iterate_links(out, content)


import requests, re, os, json
from bs4 import BeautifulSoup

def get_company_div(se_code, base_url):
    search_url = base_url + 'ara/' + se_code.lower() + '/'
    max_pages = 50
    for i in range(1, max_pages):
        try:
            url = search_url + str(i)
            page = requests.get(url)
        except:
            return 'No such div.'

        content = page.text
        soup = BeautifulSoup(content, 'html.parser')
        divs = list(soup.findAll("div", {"class": "searchResult company"}))

        for div in divs:
            div_soup = BeautifulSoup(str(div), 'html.parser')
            scode_divs = list(div_soup.findAll("div", {"class": "stockCode"}))
            for scode_div in scode_divs:
                if str(scode_div).lower().find(se_code) != -1:
                    company_div = div
        return str(company_div)

def get_company_id(se_code, base_url):
    company_div = get_company_div(se_code, base_url)
    if company_div == 'No such div.':
        return 'No such id.'

    soup = BeautifulSoup(company_div, 'html.parser')
    links = []
    for anchor in soup.findAll('a', href=True):
        links.append(anchor['href'])
    
    for link in links:
        if str(link).find('/tr/sirket-bilgileri/genel/') != -1:
            return str(link)[27:]

    return 'No such id.'


def get_notification_url(se_code, base_url):
    company_id = get_company_id(se_code, base_url)
    if company_id == 'No such id.':
        return 'No such id.'
    url = base_url + 'bildirim-sorgu?member=' + company_id + '&disclosureClass=FR'
    return url

def download_financial_files(data_path, se_code, base_url):
    company_id = get_company_id(se_code, base_url)
    notification_url = get_notification_url(se_code, base_url)
    print('notification url: ', notification_url)
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Referer': notification_url,
        'Origin' : 'https://www.kap.org.tr',
        'Content-Type' : 'application/json;charset=UTF-8',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Host' : 'www.kap.org.tr'
    })

    endpoint_url = 'https://www.kap.org.tr/tr/api/memberDisclosureQuery'
    
    request_json = json.dumps({  
        "fromDate":"2017-12-02",
        "toDate":"2018-12-02",
        "year":"",
        "term":"",
        "ruleType":"",
        "bdkReview":"",
        "disclosureClass":"FR",
        "index":"",
        "market":"",
        "isLate":"",
        "subjectList":[],
        "mkkMemberOidList":[  
            company_id
        ],
        "inactiveMkkMemberOidList":[  
        ],
        "bdkMemberOidList":[  
        ],
        "mainSector":"",
        "sector":"",
        "subSector":"",
        "memberType":"IGS"
    })
    
    response = session.post(endpoint_url, request_json)
    
    for notification in response.json():
        if notification['subject'].find('Faaliyet Raporu') != -1:
            filename = notification['stockCodes'] + '_Faaliyet_Raporu_'
            download_financial_file(base_url, 
                notification['disclosureIndex'], data_path, filename)
            break

    for notification in response.json():
        if notification['subject'].find('Finansal Rapor') != -1:
            filename = notification['stockCodes'] + '_Finansal_Rapor_'
            download_financial_file(base_url, 
                notification['disclosureIndex'], data_path, filename)
            break


def download_financial_file(base_url, disclosure_index, data_path, filename):
    url = base_url + 'Bildirim/' + str(disclosure_index)
    path = os.path.join(data_path, filename + '.pdf')
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')
    
    links = []
    for anchor in soup.findAll('a', href=True):
        links.append(anchor['href'])

    for link in links:
        if link.find('/tr/ek-indir/') != -1:
            url = base_url + link[4:]
            response = requests.get(url)
            with open(path, 'wb') as f:
                f.write(response.content)
                return

config = {
    'base_url': 'https://www.kap.org.tr/tr/'
}

se_code = input().lower()
current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'data')
download_financial_files(data_path, se_code, config['base_url'])

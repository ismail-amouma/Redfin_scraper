"""
a scraper of the redfin.com website using selenuim and driver manger to set it up 
"""

from constant import CITY_LINKS
import concurrent.futures
from bs4 import BeautifulSoup
import requests
import time
import re
import time 
start = time.time()

def extract_phone_and_email(text):
    contact_prefix = "Contact:"
    phone_pattern = r'\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}'
    email_pattern = r'\S+@\S+'

    # Remove "Contact:" prefix
    if text.startswith(contact_prefix):
        text = text[len(contact_prefix):]

    # Search for phone numbers using regex
    phone_matches = re.findall(phone_pattern, text)
    phone = phone_matches[0] if phone_matches else "Phone number not available"

    # Search for email addresses using regex
    email_matches = re.findall(email_pattern, text)
    email = email_matches[0] if email_matches else "Email not available"

    return phone, email

def get_table_links(soup):
    
    links=[]
    table=soup.find_all('a', class_='slider-item')
    for row in table:
        links.append(row["href"])
    return links

def scrape_table_links(link):
    
        re = requests.get(link)
        soup = BeautifulSoup(re.content, "html.parser")
        return get_table_links(soup)


def scrape_all_tables_links(location):
    link = CITY_LINKS[location]
    all_links = set()
    urls_to_scrape = [[link + f"/page-{i}"  for i in range(1, 10)] for _ in range(10)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
            for list in urls_to_scrape:
                all_links.update(*executor.map(scrape_table_links, list))
                time.sleep(5)
    return all_links

def scrape_page(soup,link):
    try:

        adresse = soup.find("div", class_="bp-homeAddress")
        address_parts = adresse.get_text().split(',')
        street_address = address_parts[0].strip()
        city = address_parts[1].strip()
        state_zip = address_parts[2].strip()
        state, zip_code = state_zip.split(' ', 1)
    except:
        parts = link.split("/")
        state = parts[1]
        city = parts[2]
        address_and_zip = parts[3].split("-")
        street_address = " ".join(address_and_zip[1::])
        zip_code = address_and_zip[0]



    try:

        stat_value = soup.find_all("div", class_="statsValue")
        price = stat_value[0].get_text()
        beds = stat_value[1].get_text()
        if beds == "—":
            beds = "beds not available"

        baths = stat_value[2].get_text()
        if baths == "—":
            baths = "baths not available"
    except:
        price = "price not available"
        beds = "beds not available"
        baths = "baths not available"
    try:
        stat_size = soup.find("div", class_="stat-block sqft-section")
        size = stat_size.get_text().replace('\n', ' ').strip()
        if size == "— Sq Ft":
            size = ""
    except:
        size = ""
    try:
        text3=soup.find("span", class_="agent-basic-details--heading").span.get_text()
        agent_name = text3.split(" ")[0]
        agent_last_name=text3.split(" ")[1]
    except:
        try:
            text3=  soup.find("div", class_="agent-info-item flex flex-wrap").span.a.get_text()
            agent_name = text3.split(" ")[0]
            agent_last_name=text3.split(" ")[1]
        except:
            agent_name = "agent_name not available"
            agent_last_name="agent_last_name not available"


    try:
        agent_contact_info = soup.find("div", class_="listingContactSection").get_text()
        agent_phone, agent_email = extract_phone_and_email(agent_contact_info)
    except:
        try:
            agent_phone = soup.find("div", class_="phone-numbers").find_all("span", class_="")[0].a.get_text()
        except:
            try:
                agent_phone = soup.find("a", class_="phone-number TextOrCallPhoneLink").get_text()
            except:

                agent_phone = "Phone number not available"
        try:
            agent_email = soup.find("div", class_="email-addresses").find_all("span", class_="")[0].a.get_text()
        except:
            agent_email = "email not available"




    time_on_redfin = 'None'
    property_type = 'None'
    year_built = 'None'
    style = 'None'
    community = 'None'
    lot_size = 'None'
    try:    
        labels = ["Time on Redfin", "Property Type", "Year Built", "Style", "Community", "Lot Size"]
        table = soup.find("div", class_="DPTableDisplay").find_all("div", class_="table-row")
        lables=[text.span.get_text() for text in table]
        values=[text.span.next_sibling.get_text() for text in table]
        for i, lable in enumerate(lables):
            if lable in labels:
                value = values[i]
                if lable == "Time on Redfin":
                    time_on_redfin = value
                elif lable == "Property Type":
                    property_type = value
                elif lable == "Year Built":
                    year_built = value
                elif lable == "Style":
                    style = value
                elif lable == "Community":
                    community = value
                elif lable == "Lot Size":
                    lot_size = value
    except:
        pass
    scraped_data = {
        "time_on_redfin": time_on_redfin,
        "property_type": property_type,
        "year_built": year_built,
        "style": style,
        "community": community,
        "lot_size": lot_size,
        "street_address": street_address,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "price": price,
        "beds": beds,
        "baths": baths,
        "size": size,
        "agent_name": agent_name,
        "agent_last_name":agent_last_name,
        "agent_phone": agent_phone,
        "agent_email": agent_email
    }
    return scraped_data
def scrape_link(link, index,len):
    print(f"Scraping link {index}/{len}")
    session = requests.Session()
    session.cookies.clear()
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    response = session.get("https://www.redfin.com"+link,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    scraped_data = scrape_page(soup,link)
    return scraped_data
def get_data(location):
    scraped_data=[]
    links=list(scrape_all_tables_links(location))
    j=len(links)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i, link in enumerate(links):
            future = executor.submit(scrape_link, link, i+1, j)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                scraped_data.append(data)
            except Exception as e:
                print(f"Error scraping link: {e}")
    return scraped_data
def update_dat(location):
    state=location.split(", ")[1]
    city=location.split(", ")[0]
    scraped_data=[]
    base_link="https://www.redfin.com/sitemap/"+state+"/"+"newest-homes"
    re = requests.get(base_link)
    soup = BeautifulSoup(re.content, "html.parser")
    pages_max_number=int((soup.find_all("a", class_="PageNumber button-text"))[-1].get_text())
    for i in range(1,pages_max_number+1):
        link=base_link+"/page-"+str(i)
        req=requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        links=soup.find("ul", class_="list ldpsSection").find_all("li")
        total_link=[]
        j=len(links)
        for i,link in enumerate(links):
            link=link.div.a["href"]
            city_link=link.split("/")[2]
            if city_link[:len(city)]==city:
                total_link.append(link)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i, link in enumerate(total_link):
                future = executor.submit(scrape_link, link, i+1, j)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    scraped_data.append(data)
                except Exception as e:
                    print(f"Error scraping link: {e}")
                
    return scraped_data

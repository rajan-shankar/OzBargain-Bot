import feedparser
import time
import smtplib
import requests
from github import Github

# for committing 
my_github_token = ''
rajan_shankar = Github(my_github_token)
repo = rajan_shankar.get_repo('rajan-shankar/OzBargain-Deals-Bot')
historic_deals = repo.get_contents('historic_deals.txt')

# for retrieving
r = requests.get('https://raw.github.com/rajan-shankar/OzBargain-Deals-Bot/master/historic_deals.txt')


query = {
    ('Nintendo', 'Switch'): (300, 1000),
    ('Blue Illusion',): (0, 1000),
    ('Air Pods',): (100, 500),
    ('Lee', 'Riders'): (0, 1000),
    ('Sony', 'Headphones'): (100, 500)
}

sender = 'ozbargainbot1@outlook.com'
password = ''
recipients = ['rajan.shankar@outlook.com']


def get_prices(title):
    prices_str = ''
    to_keep = '1234567890.$'
    
    for char in title:
        if char in to_keep:
            prices_str += char
        else:
            prices_str += ' '
        
    prices_list = []
    for element in prices_str.split():
        if '$' in element:
            try:
                prices_list.append(
                    float(element.replace('$', ''))
                )
            except:
                pass
            
    return prices_list


def search_for_deals():
    ozbargain = feedparser.parse('https://www.ozbargain.com.au/deals/feed')
    for entry in ozbargain.entries:
        title = entry['title']
        summary = entry['summary']
        link = entry['link']

        for key in query:
            match = True
            for term in key:
                if term.lower() not in (title + summary).lower():
                    match = False
    
            if match:
                lower_bound = query[key][0]
                upper_bound = query[key][1]
                prices = get_prices(title)
                
                if prices:
                    match = False
                for price in prices:
                    if lower_bound < price < upper_bound:
                        match = True

            if match and (link not in found) :
                mail = smtplib.SMTP('smtp-mail.outlook.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login(sender, password)
                mail.sendmail(sender, recipients, msg='\nDeal found for search terms '+str(key)
                              +' within the specified price range '+str(query[key])+' at:\n'+link)
                mail.close()
                
                found.append(link)
                repo.update_file(
                    historic_deals.path, 
                    "automated commit",  # title of commit
                    "\n".join(found),  # content of file of commit
                    historic_deals.sha
                )

                time.sleep(10)
                break


found = r.text.split('\n')
while True:
    search_for_deals()
    time.sleep(600)
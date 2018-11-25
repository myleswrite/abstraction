import xmltodict, requests, time, json, pandas
from bs4 import BeautifulSoup

wait = 0.2
print("Hello, let's start by getting a valid sitemap")
askurl = input("Please enter a valid sitemap: ")
filename = input("What do you want to call the saved file (without .ending)?")
print("Getting the sitemap from " + askurl)
sitemapreq = requests.get(askurl) # Go get the sitemap
if sitemapreq.status_code == 200: # Did we get a valid response back?
    print('Valid response received')
    if '/xml' in sitemapreq.headers['Content-Type']:
        thexml = xmltodict.parse(sitemapreq.text,xml_attribs=True)
        print('Total items: ' + str(len(thexml['urlset']['url'])))
        if len(thexml['urlset']['url']) > 499: #Slow down if there are a lot of URLs to avoid problems.
            wait = 1
        listurl = []
        complete = []
        lineno = 0
        for key in thexml['urlset']['url']: # Create a list of urls from the sitemap
            time.sleep(wait) # Let's not flood requests?
            print('Working on url ' + key['loc'] + '\n')
            page = requests.request('GET', key['loc'])
            line = {}
            if page.status_code == 200: # Did we get a valid response back?
                content = BeautifulSoup(page.text,'html.parser')
                lineno += 1
                line= dict(
                            urlnumber = lineno,
                            modified = key['lastmod'],
                            address = key['loc'],
                            status = page.status_code,
                            title = content.title.string,
                            )
                for tag in content.head.find_all("meta"):
                    if tag.get("name", None) == "description": # Is this a meta description?
                        line['metadescription'] = tag.get("content", None)
                        line['metadescriptionlength'] = len(tag.get("content", None))
                complete.append(line)
            else:
                lineno += 1
                line = dict(
                            urlnumber = lineno,
                            modified = key['lastmod'],
                            address = key['loc'],
                            status = page.status_code,
                            title = '',
                            metadescription ='',
                            metadescriptionlength = ''
                            )
        print(json.dumps(complete))
        # Attempt to create a JSON
        jsonname = filename + '.json'
        f = open(jsonname,"w+")
        f.write(json.dumps(complete))
        f.close
        print("Saved JSON")
        # Attempt to create a CSV
        csvname = filename + '.csv'
        pandas.DataFrame(complete).to_csv(csvname, index=False)
        print("Saved CSV")
    else:
        print('Invalid response')
exit()

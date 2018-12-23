# -*- coding: utf-8 -*-

#Import the required modules. I will tidy this up into a loop at some point

try:  # For converting the XML to a dictionary
    import xmltodict
except:
    print("xmltodict is required")
    exit()
try:  # For getting the URL response
    import requests
except:
    print("requests is required")
    exit()
try:  # For waiting
    import time
except:
    print("time is required")
    exit()
try:  # For saving as json
    import json
except:
    print("json is required")
    exit()
try:  # For saving as CSV
    import pandas
except:
    print("pandas is required")
    exit()
try: # For getting the meta descriptions
    from bs4 import BeautifulSoup
except:
    print("BeautifulSoup is required")
    exit()
try: # For the save as option
    from tkinter.filedialog import asksaveasfilename
except:
    print("tkinter.filedialog is required")
    exit()


wait = 0.2
print("Hello, let's start by getting a valid sitemap")
askurl = input("Please enter a valid sitemap (there is no error checking here if you don't enter a valid URL): ")
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
                            address = key['loc'],
                            status = page.status_code,
                            title = content.title.string,
                            )
                for tag in content.head.find_all("meta"):
                    if tag.get("name", None) == "description": # Is this a meta description?
                        line['metadescription'] = tag.get("content", None)
                        line['metadescriptionlength'] = len(tag.get("content", None))
                complete.append(line)
                if 'lastmod' in key : #Is lastmod blank?
                    line['modified'] = key['lastmod']
                else:
                    line['modified'] = '0'
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
        # Are we saving this anywhere?
        dosave = input("Do you want to save a JSON and CSV — Type 'Y' for yes or anything else for no. ")
        if dosave == 'Y' or dosave =='y': #If we're saving let's save
            file_name = asksaveasfilename()
            # Attempt to create a JSON
            jsonname = file_name + '.json'
            f = open(jsonname,"w+")
            f.write(json.dumps(complete))
            f.close
            print("Saved JSON")
            #Attempt to create a CSV
            csvname = file_name + '.csv'
            pandas.DataFrame(complete).to_csv(csvname, index=False)
            print("Saved CSV")
        else:
            print("Okay we're done here.")
    else:
        print('Invalid response')
exit()

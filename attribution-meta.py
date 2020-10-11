# -*- coding: utf-8 -*-

#Import the required modules.

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
heads = {
    'User-Agent': 'attribution meta check crawler',
    }

print("Hello, let's start by getting a valid sitemap")
askurl = input("Please enter a valid sitemap (there is no error checking here if you don't enter a valid URL): ")
print("Getting the sitemap from " + askurl)
sitemapreq = requests.get(askurl,timeout=5.00,headers=heads) # Go get the sitemap
if sitemapreq.status_code == 200: # Did we get a valid response back?
    print('Valid response received. Hang on a minute please.')
    if '/xml' in sitemapreq.headers['Content-Type']:
        thexml = xmltodict.parse(sitemapreq.text,xml_attribs=True)
        print('Total items: ' + str(len(thexml['urlset']['url'])))
        totes = len(thexml['urlset']['url'])
        if len(thexml['urlset']['url']) > 499: #Slow down if there are a lot of URLs to avoid problems.
            wait = 0.5
        listurl = []
        lineno = 0
        # Choose a filename for saving (will replace with a dialog at some point
        print("What is the filename for saving the tab delimited file (without .txt)?")
        savefile = input()
        savefile += ".txt"
        with open(savefile, 'a+') as w: # Add a header line
            w.write("urlnumber\taddress\tstatus\ttitle\tmetadescription\tmetadescriptionlength\tmodified" + "\n")
            w.close
        for key in thexml['urlset']['url']: # Create a list of urls from the sitemap
            time.sleep(wait) # Let's not flood requests?
            print('Working on url ' + key['loc'] + '\n')
            try:
                if '.pdf' not in key['loc']:
                    page = requests.get(key['loc'],timeout=8.00,headers=heads)
                    print(page.text)
                    lineno += 1
                    line = dict(
                        urlnumber = lineno,
                        address = key['loc'],
                        status = page.status_code,
                    )
                    if 'lastmod' in key : #Is lastmod blank?
                        line['modified'] = key['lastmod']
                    else:
                        line['modified'] = '0'
                    if page.status_code == 200: # Did we get a valid response back?
                        content = BeautifulSoup(page.text,'html.parser')
                        try:
                            line['title'] = content.title.string
                        except:
                            line['title'] = 'No title'
                        line['metadescription'] = ''
                        line['metadescriptionlength'] = ''
                        try:
                            for tag in content.head.find_all("meta"):
                                if tag.get("name", None) == "description": # Is this a meta description?
                                    line['metadescription'] = tag.get("content", None)
                                    line['metadescriptionlength'] = len(line['metadescription'])
                        except:
                            line['metadescription'] = ''
                            line['metadescriptionlength'] = '0'
                        metadescript = str(line['metadescription'])
                        metalen = str(line['metadescriptionlength'])
                        print(metadescript + "\n")
                    else:
                        line['title'] = ''
                        line['metadescription'] = ''
                        line['metadescriptionlength'] = ''
                    with open(savefile, 'a+') as w: # Add a new line to the file
                        w.write(str(line['urlnumber']) + "\t" + str(line['address']) + "\t" + str(line['status']) + "\t" + str(line['title']) + "\t" + metadescript + "\t" + metalen + "\t" + str(line['modified']) + "\n")
                        w.close
            except requests.exceptions.RequestException as e:  # If there's an error print it
                print (e)
    else:
        print('Invalid header response (probably no /xml in Content Type)')
print("Finished.")
exit()

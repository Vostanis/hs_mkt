from vault import API_KEY

import zipfile
import os
import pandas as pd
import requests

'''
Available Datasets
==================
         name                                              title
0        ccod  UK companies that own property in England and ...
1        ocod  Overseas companies that own property in Englan...
2         nps                           National Polygon Service
3  nps_sample                    National Polygon Service Sample
4     res_cov                              Restrictive Covenants
5      leases                                  Registered Leases

rsp0 = requests.get(url=URL_DATASETS, headers=headers)
data = (rsp0.json())['result']
dsdf = pd.DataFrame(data)
'''

# URLs
URL_DATASETS = "https://use-land-property-data.service.gov.uk/api/v1/datasets"
URL_UK = "https://use-land-property-data.service.gov.uk/api/v1/datasets/ccod"
URL_OVERSEAS = "https://use-land-property-data.service.gov.uk/api/v1/datasets/ocod"
URL_LEASES = "https://use-land-property-data.service.gov.uk/api/v1/datasets/leases"

# Auth
headers = {
    'Authorization': f'{API_KEY}'
}

# Paths
current_p = os.getcwd()
parent_p = os.path.dirname(current_p)
data_p = parent_p + '/data'
live_data_p = data_p + '/live'
dump_data_p = data_p + '/dump'

os.makedirs(data_p, exist_ok = True)
os.makedirs(live_data_p, exist_ok = True)
os.makedirs(dump_data_p, exist_ok = True)

# Loop through all the files and write them into /dump
rsp1 = requests.get(url=URL_UK, headers=headers)
ukdf = pd.DataFrame(rsp1.json()['result']['resources']) 
FILE_UK = URL_UK + '/'  + ukdf['file_name'].astype(str)
for i in FILE_UK.index: 
    url = FILE_UK.iloc[i]
    file = os.path.basename(url)
    filepath = dump_data_p + '/' + file
    print(f"Downloading: {file} ...")
    rspi = requests.get(url=url, headers=headers)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Removing {filepath} ...")

    with open(filepath, 'wb') as f:
        print(f"Writing: {file} ...")
        f.write(rspi.content)
# Currently only UK datasets

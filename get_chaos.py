# Author : 

import os, json, requests, zipfile
from multiprocessing.dummy import Pool

ASSERT_PATH = "asserts_baixiaomao"
SILENT_MODE = 0  # if 0:print logs , if 1:print nothing

chaos_url = "https://chaos-data.projectdiscovery.io/index.json"
resp_json = json.loads(requests.get(chaos_url).text)
asserts_with_money = filter(lambda info: info["bounty"], resp_json)

if not os.path.exists(ASSERT_PATH):
    os.makedirs(ASSERT_PATH + "/zipfiles")
    os.makedirs(ASSERT_PATH + "/unzipped")


def unzip_file(zip_src, dst_dir):
    if zipfile.is_zipfile(zip_src):
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        if not SILENT_MODE:
            print("[*]Unzip zip file ok : " + zip_src + " => " + dst_dir)


def dld_zip(info, path_name=ASSERT_PATH):
    file_name = path_name + "/zipfiles/" + info["name"] + ".zip"
    with open(file_name, "wb") as f:
        f.write(requests.get(info["URL"], stream=True).content)
    if not SILENT_MODE:
        print("[*]Download zip file ok : " + info["name"])


with Pool(20) as p:
    p.map(dld_zip, list(asserts_with_money))

for f in os.listdir(ASSERT_PATH + "/zipfiles/"):
    unzip_file(ASSERT_PATH + "/zipfiles/" + f, ASSERT_PATH + "/unzipped/" + f[:-4])

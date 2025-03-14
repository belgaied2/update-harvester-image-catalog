from bs4 import BeautifulSoup
import requests
import re

version_regex = r'\d\.\d'
baseurls = ['https://download.rockylinux.org/pub/rocky/','https://dl.rockylinux.org/vault/rocky/']
images_path = 'images/x86_64/'
image_name_regex = r'Rocky-[8|9]-GenericCloud(-Base|)[-|\.]('+version_regex+'\-(\d{8}\.\d)|latest)\.x86_64.qcow2$'

def get_rocky_image_list():
  print('Building RockyLinux list ...')
  version_list = dict()
  for baseurl in baseurls:
    release_page = requests.get(baseurl)
    soup = BeautifulSoup(release_page.text, 'html.parser')
    versions = soup.find_all('a')
  
    for version in versions:
      version_string = version.get('href')
      match = re.match(version_regex+'/$', version_string)
      if match:
        version_list[version_string] = baseurl+version_string+images_path
  
  #print(version_list)
  #print(re.match(image_name_regex, 'Rocky-9-GenericCloud-Base-9.1-20221123.0.x86_64.qcow2'))
  matching_image_list = []
  for version_path in version_list:
    version = version_path.replace('/','')
    #print(version_list[version_path])
    version_images_page = requests.get(version_list[version_path])
    version_soup = BeautifulSoup(version_images_page.text, 'html.parser')
    for image_name in version_soup.find_all('a'):
      name_match = re.match(image_name_regex, image_name.get('href'))
      if name_match:
        image = {"version": version, "shortName": "Rocky Linux "+version, "url":version_list[version_path] + image_name.get('href'), "build":name_match[2]}
        #matching_image_list.append(version_list[version_path] + image_name.get('href'))
        matching_image_list.append(image)

  print('Finished Building RockyLinux image list!\n---')
  return {"RockyLinux": matching_image_list}

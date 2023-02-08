import requests
from bs4 import BeautifulSoup
import re

baseurl = 'https://cloud-images.ubuntu.com/minimal/releases/'
version_line_regex = '\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}    -   Ubuntu (Minimal|Server) (\d{2}\.\d{2}) (LTS |)\([A-Za-z ]*\) (released|daily) builds\s*(\[END OF LIFE\]){0,1}$'
filename_regex = 'ubuntu-\d{2}\.\d{2}-minimal-cloudimg-amd64.img'

def get_ubuntu_image_list():
  print('Building Ubuntu list ...')
  minimal_response = requests.get(baseurl)
  minimal_page = BeautifulSoup(minimal_response.content, 'html.parser')
  image_lines = minimal_page.find('pre').find_all('a')
  
  # Selecting not "END OF LIFE" images
  selected_image_lines = dict()
  for image_line in image_lines:
    description = image_line.next.next.text
    match = re.match(version_line_regex, description)
    if match:
      #print(description)
      if match.group(5) == None:
        #print('Adding to List') 
        selected_image_lines[match.group(2)] = {
          'version_name':image_line.text.replace('/',''), 
          'version_number': match.group(2), 
          'LTS': match.group(3) == 'LTS ', 
          'url': baseurl+image_line.get('href')+'release/'
          }

  # Accessing non-"END OF LIFE" image folder
  ubuntu_list = []
  for image_url in selected_image_lines:
    #print(selected_image_lines[image_url])
    image_page = requests.get(selected_image_lines[image_url]['url'])
    #print(image_page)
    links = BeautifulSoup(image_page.content, 'html.parser').find_all('a')
    for link in links:
      #print(link)
      match = re.match(filename_regex, link.get('href'))
      if match:
        #print(link.get('href'))
        ubuntu_list.append({
          'version': selected_image_lines[image_url]['version_number'],
          'shortName': 'Ubuntu '+selected_image_lines[image_url]['version_name']+' '+ selected_image_lines[image_url]['version_number'],
          'url': selected_image_lines[image_url]['url'] + link.get('href'),
          'build': 'latest'
          })

  print('Finished Building Ubuntu image list!\n---')
  return {'ubuntu': ubuntu_list}

#print(get_ubuntu_image_list())
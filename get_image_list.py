import json
import requests
import re

baseurl = dict()
baseurl["leap"] = 'https://download.opensuse.org/download/distribution/leap/'
jstable = '?jsontable'
leap_image_name_regex = 'openSUSE-Leap-([0-9\.]{4})-JeOS.x86_64-[0-9\.]{4}-OpenStack-Cloud-(.*).qcow2$'
leap_short_name = 'OpenSUSE Leap JeOS'

leap_get = requests.get(baseurl['leap'] + '?jsontable').json()
#print(leap_get)

result_images = []
for leap_data in leap_get['data']:
    #print(leap_data['name'])
    version_get = requests.get(baseurl['leap']+leap_data['name']+'appliances'+jstable)
    if version_get.status_code == 200:
      #print(version_get.json()['data'])
      for leap_image in version_get.json()['data']:
        #print(leap_image['name'])
        match = re.match(leap_image_name_regex , leap_image['name'])
        if match:
          version_result = dict()
          version_result['version'] = match[1]
          version_result['shortName'] = leap_short_name+' '+match[1]
          version_result['url'] = baseurl['leap']+leap_data['name']+'appliances/'+leap_image['name']
          version_result['build'] = match[2]
          #print(version_result)
          result_images.append(version_result)
leap_result = dict(leap=result_images)

print('Writing output file ...')
output_file = open('image-metadata.json','w')
json.dump(leap_result, output_file, indent=2)
print('Image Metadata file written successfully!')
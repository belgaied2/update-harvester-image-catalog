import json
import requests
import re

data = {'leap': { 
          'baseurl':'https://download.opensuse.org/download/distribution/leap/', 
          'regex': r'openSUSE-Leap-([0-9\.]{4})-JeOS.x86_64-[0-9\.]{4}-(OpenStack-)*Cloud-(.*).qcow2$',
          'shortName': 'OpenSUSE Leap JeOS'
        },
        'leap15.4+':{
          'baseurl': 'https://download.opensuse.org/download/distribution/leap/',
          'regex': r'openSUSE-Leap-([0-9\.]{4})-Minimal-VM.x86_64-(OpenStack-)*Cloud.qcow2$',
          'shortName': 'OpenSUSE Leap Minimal'
        },
        'tumbleweed':{
          'baseurl': 'https://download.opensuse.org/tumbleweed/',
          'regex': r'openSUSE-Tumbleweed-Minimal-VM.x86_64-Cloud.qcow2$',
          'shortName': 'OpenSUSE Tumbleweed'
        },
        'microos':{
          'baseurl': 'https://download.opensuse.org/tumbleweed/',
          'regex': r'openSUSE-MicroOS.x86_64-OpenStack-Cloud.qcow2$',
          'shortName': 'OpenSUSE MicroOS'
        }
}
jstable = '?jsontable'

def get_suse_image_list() :
  print('Building OpenSUSE list ...')
  opensuse_result = dict()
  for distro in data:
    leap_get = requests.get(data[distro]['baseurl'] + '?jsontable').json()
    result_images = []
    if distro in ['tumbleweed','microos']:
        leap_get['data'] = [{'mtime':0, 'name': '', 'size':0}]
    #print(leap_get['data'])
    for leap_data in leap_get['data']:
        #print(leap_data['name'])
        version_get = requests.get(data[distro]['baseurl']+leap_data['name']+'appliances'+jstable)
        if version_get.status_code == 200:
          #print(version_get.json()['data'])
          for leap_image in version_get.json()['data']:
            #print(leap_image['name'])
            matchVersion = re.match(data[distro]['regex'] , leap_image['name'])
            matchBuild = re.match('.*([B,b]uild.*).qcow2' , leap_image['name'])
            if matchBuild:
              build = matchBuild[1]
            else:
              build = 'current'
            if matchVersion:
              #print(leap_image['name'])
              version_result = dict()
              try:
                version_result['version'] = matchVersion[1]
                version_result['build'] = build
                version_result['shortName'] = data[distro]['shortName']+' '+matchVersion[1]
              except IndexError:
                version_result['version'] = 'current'
                version_result['build'] = 'current'
                version_result['shortName'] = data[distro]['shortName']
              version_result['url'] = data[distro]['baseurl']+leap_data['name']+'appliances/'+leap_image['name']
              #print(version_result)
              result_images.append(version_result)

    opensuse_result[distro] = result_images
  print('Finished Building OpenSUSE image list!\n---')
  return opensuse_result


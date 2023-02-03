import json
import opensuse


print('Writing output file ...')
output_file = open('image-metadata.json','w')
json.dump(opensuse.get_suse_image_list(), output_file, indent=2)
print('Image Metadata file written successfully!')


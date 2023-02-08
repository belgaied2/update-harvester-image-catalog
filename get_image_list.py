import json
import opensuse
import rocky
import ubuntu

print('Writing output file ...\n---')
output_file = open('image-metadata.json','w')

final_content = {"HarvesterImageCatalog":
                 {
                    **opensuse.get_suse_image_list() , 
                    **rocky.get_rocky_image_list(),
                    **ubuntu.get_ubuntu_image_list()
                  }
                }

json.dump(final_content, output_file, indent=2)
print('Image Metadata file written successfully!')



# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. h5m files created in this way are imprinted,
# merged, faceted and ready for use in OpenMC. One of the key aspects of this
# is the asssignment of materials to the volumes present in the CAD files.

from cad_to_h5m import cad_to_h5m
import json

with open('stage_1_output/manifest.json') as json_file:
    neutronics_description = json.load(json_file)

list_of_components = ['stage_1_output/divertor.stp', 'stage_1_output/blanket.stp']

# modifies the names of the stp files to include the output dir
for entry in neutronics_description:
    entry['cad_filename'] = 'stage_1_output/' + entry['cad_filename']
    if entry['cad_filename'] in list_of_components:
        entry['tet_mesh'] = "size 40"

cad_to_h5m(
    files_with_tags=neutronics_description,
    make_watertight=True,
    h5m_filename='stage_2_output/dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
    cubit_filename='stage_2_output/unstructured_mesh.cub'
)


# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
from cad_to_h5m import cad_to_h5m

my_reactor = paramak.BallReactor(
    inner_bore_radial_thickness=1,
    inboard_tf_leg_radial_thickness=30,
    center_column_shield_radial_thickness=60,
    divertor_radial_thickness=50,
    inner_plasma_gap_radial_thickness=30,
    plasma_radial_thickness=300,
    outer_plasma_gap_radial_thickness=30,
    plasma_gap_vertical_thickness=30,
    firstwall_radial_thickness=3,
    blanket_radial_thickness=100,
    blanket_rear_wall_radial_thickness=3,
    elongation=2.75,
    triangularity=0.5,
    number_of_tf_coils=16,
    rotation_angle=360
)

stp_filenames = my_reactor.export_stp()

# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. h5m files created in this way are imprinted,
# merged, faceted and ready for use in OpenMC. One of the key aspects of this
# is the assignment of materials to the volumes present in the CAD files.

files_with_tags = [{'cad_filename':stp_filename, 'material_tag':name} for name, stp_filename in zip(my_reactor.name, stp_filenames)]
# produces a list of dictionaries of with cad_filename and material_tag as the keys.
# the values are the stp filename and the name of the component

# modifies files_with_tags to include tet_mesh key for the blanket entry
for entry in files_with_tags:
    if entry['cad_filename'] == 'blanket.stp':
        entry['tet_mesh'] = "size 15"

cad_to_h5m(
    files_with_tags=files_with_tags,
    make_watertight=True,
    h5m_filename='stage_2_output/dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
    cubit_filename='stage_2_output/unstructured_mesh.cub'
)

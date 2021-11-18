
# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
from stl_to_h5m import stl_to_h5m

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


# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. There are two methods of creating the h5m files.
# In both cases the resulting h5m geometry mesh has volumes tagged with
# material tags.

# method 1
# makes a dagmc geometry that has not been imprinted and merged

stl_filenames = my_reactor.export_stl()
# removes the plasma as this complicates the geometry and has minimal interations with particles
stl_filenames.remove('plasma.stl')
compentent_names = my_reactor.name
compentent_names.remove('plasma')

stl_to_h5m(
    files_with_tags=[(stl_filename, name) for name, stl_filename in zip(compentent_names, stl_filenames)],
    h5m_filename='dagmc_not_merged.h5m',
)


# method 2
# makes a dagmc geometry that has been imprinted and merged and requires cubit
# from cad_to_h5m import cad_to_h5m
# stp_filenames = my_reactor.export_stp()

# # removes the plasma as this complicates the geometry and has minimal interations with particles
# stp_filenames.remove('plasma.stp')

# files_with_tags = [{'cad_filename': stp_filename, 'material_tag': name} for name, stp_filename in zip(compentent_names, stp_filenames)]
# # produces a list of dictionaries of with cad_filename and material_tag as the keys.
# # the values are the stp filename and the name of the component

# cad_to_h5m(
#     files_with_tags=files_with_tags,
#     make_watertight=True,
#     h5m_filename='dagmc.h5m',
#     cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
# )

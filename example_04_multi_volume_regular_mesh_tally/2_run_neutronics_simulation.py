# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops


geometry = odw.Geometry(h5m_filename='dagmc.h5m')

# this links the material tags in the dagmc h5m file with materials.
# these materials are input as strings so they will be looked up in the
# neutronics material maker package
material_tag_to_material_dict = {
    "mat_inboard_tf_coils": "copper",
    "mat_center_column_shield": "tungsten",
    "mat_firstwall": "tungsten",
    "mat_blanket": "Li4SiO4",
    "mat_blanket_rear_wall": "eurofer",
    "mat_divertor_upper": "tungsten",
    "mat_divertor_lower": "tungsten",
}

materials = odw.Materials(
    h5m_filename=geometry.h5m_filename,
    correspondence_dict=material_tag_to_material_dict,
)

# uncomment if you don't have nuclear data already and it will be downloaded
# import openmc_data_downloader as odd
# odd.just_in_time_library_generator(
#     libraries=['ENDFB-7.1-NNDC', 'TENDL-2019'],
#     materials=materials
# )

# gets the corners of the geometry for use later
bounding_box = geometry.corners()

tally1 = odw.MeshTally3D(
    mesh_resolution=(100, 100, 100),
    bounding_box=bounding_box,
    tally_type="(n,Xa)",
)

tally2 = odw.MeshTally2D(tally_type="(n,Xa)", plane="xy", bounding_box=bounding_box)

tally3 = odw.MeshTally2D(tally_type="(n,Xa)", plane="xz", bounding_box=bounding_box)

tallies = openmc.Tallies([tally1, tally2, tally3])

settings = odw.FusionSettings()
settings.batches = 4
settings.particles = 10000
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350, angles=(0, 3.14))


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
statepoint_file = my_model.run()

print(f'neutronics results are saved in {statepoint_file}')

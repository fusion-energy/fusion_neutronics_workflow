# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops


# could set to dagmc.h5m if the imprinted and merged geometry is preferred
my_h5m_filename = 'dagmc_not_merged.h5m'

# this links the material tags in the dagmc h5m file with materials.
# these materials are input as strings so they will be looked up in the
# neutronics material maker package
material_tag_to_material_dict = {
    'plasma':'DD_plasma',
    'inboard_tf_coils':'copper',
    'center_column_shield':'tungsten',
    'firstwall':'tungsten',
    'blanket':'Li4SiO4',
    'blanket_rear_wall':'eurofer',
    'divertor':'tungsten'
}

geometry = odw.Geometry(h5m_filename=my_h5m_filename)

materials = odw.Materials(
    # h5m_filename='dagmc.h5m',
    h5m_filename=my_h5m_filename,
    correspondence_dict=material_tag_to_material_dict
)

tally1 = odw.MeshTally3D(
    mesh_resolution=(100, 100, 100),
    bounding_box=my_h5m_filename,
    tally_type="(n,Xa)",
)

tally2 = odw.MeshTally2D(
    tally_type="(n,Xa)",
    plane="xy",
    bounding_box=my_h5m_filename
)

tally3 = odw.MeshTally2D(
    tally_type="(n,Xa)",
    plane="xz",
    bounding_box=my_h5m_filename
)

tallies = openmc.Tallies([tally1, tally2, tally3])

settings = odw.FusionSettings()
settings.batches = 4
settings.particles = 1000000
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
statepoint_file = my_model.run()

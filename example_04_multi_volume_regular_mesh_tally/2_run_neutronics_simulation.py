# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_post_processor as opp


# this links the material tags in the dagmc h5m file with materials.
# these materials are input as strings so they will be looked up in the
# neutronics material maker package
material_tag_to_material_dict = {
    'plasma':'DT_plasma',
    'inboard_tf_coils':'copper',
    'center_column_shield':'tungsten',
    'firstwall':'tungsten',
    'blanket':'Li4SiO4',
    'blanket_rear_wall':'eurofer',
    'divertor':'tungsten'
}

geometry = odw.Geometry(h5m_filename='dagmc.h5m')

materials = odw.Materials(
    h5m_filename='dagmc.h5m',
    correspondence_dict=material_tag_to_material_dict
)

tally1 = odw.MeshTally3D(
    mesh_resolution=(100, 100, 100),
    bounding_box=None,
    tally_type="(n,Xa)",
)

tallies = openmc.Tallies([tally1])

settings = odw.FusionSettings()
settings.batches = 4
settings.particles = 1e4
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()


# starts the simulation
statepoint_file = my_model.run()

# loads up the statepoint file with simulation results
statepoint = opp.StatePoint(filepath=statepoint_file)

# gets the first tally using its name
my_tally_1 = statepoint.get_tally(name="")

# gets number of neutron for a 1.3 mega joule shot
source_strength = opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6)

# converts the flux units of the tally
result = statepoint.process_tally(
    source_strength=source_strength,
    tally=my_tally_1,
    required_units="n,Xa reactions per cm3",
)

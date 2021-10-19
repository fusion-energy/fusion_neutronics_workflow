# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_post_processor as opp
from regular_mesh_plotter import plot_mesh, plot_stl_slice, get_tally_extent


# could set to dagmc.h5m if the imprinted and merged geometry is wanted
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
    tally_type="(n,Xa)", plane="xy", bounding_box=my_h5m_filename
)

tallies = openmc.Tallies([tally1, tally2])

settings = odw.FusionSettings()
settings.batches = 4
settings.particles = 1000
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)


# starts the simulation
statepoint_file = my_model.run()

# loads up the statepoint file with simulation results
statepoint = opp.StatePoint(filepath=statepoint_file)

# gets the first tally using its name
my_tally_1 = statepoint.get_tally(name="(n,Xa)_on_2D_mesh_xy")

# gets number of neutron for a 1.3 mega joule shot
source_strength = opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6)

# converts the flux units of the tally
result = statepoint.process_tally(
    tally=my_tally_1,
)

stl_slice = plot_stl_slice(
    stl_or_mesh='entire_geometry.stl',
    plane_origin = None,
    plane_normal = [0, 0, 1],
    rotate_plot = 0,
    filename='slice.png'
)

extent = get_tally_extent(my_tally_1)
print(extent)
plot_mesh(
    extent=extent,
    values= result,
    scale=None,  # LogNorm(),
    vmin=None,
    label="picosievert / cm / pulse",
    base_plt=stl_slice,
    filename= 'test.png',
#     vmin=1e6,
)

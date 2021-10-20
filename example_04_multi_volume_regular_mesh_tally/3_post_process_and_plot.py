
import openmc_post_processor as opp
from regular_mesh_plotter import (get_tally_extent,
                                  plot_regular_mesh_tally_with_geometry)

# can be used to scale the color scale
# from matplotlib.colors import LogNorm

statepoint_file = "statepoint.4.h5"

# loads up the statepoint file with simulation results
statepoint = opp.StatePoint(filepath=statepoint_file)

# gets the first tally using its name
my_tally_1 = statepoint.get_tally(name="(n,Xa)_on_2D_mesh_xy")

# gets number of neutron for a 1.3 mega joule shot
source_strength = opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6)


result = statepoint.process_tally(
    tally=my_tally_1,
)

extent = get_tally_extent(my_tally_1)

plot = plot_regular_mesh_tally_with_geometry(
    mesh_file_or_trimesh_object='dagmc_not_merged.h5m',
    plane_origin = None,
    plane_normal = [0, 0, 1],
    rotate_plot = 0,
    extent=extent,
    values= result,
    # scale=LogNorm(),
    vmin=None,
    label="picosievert / cm / pulse",
    filename= 'test.png',
)

plot.show()

import openmc_tally_unit_converter as otuc
import openmc
from regular_mesh_plotter import plot_regular_mesh_tally_with_geometry

# can be used to scale the color scale
from matplotlib.colors import LogNorm

statepoint_file = "statepoint.4.h5"

# loads up the statepoint file with simulation results
statepoint = openmc.StatePoint(filepath=statepoint_file)

# gets the first tally using its name
my_tally_xy = statepoint.get_tally(name="(n,Xa)_on_2D_mesh_xy")
my_tally_xz = statepoint.get_tally(name="(n,Xa)_on_2D_mesh_xz")

# gets number of neutron for a 1.3 mega joule shot
source_strength = otuc.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6)


plot = plot_regular_mesh_tally_with_geometry(
    tally=my_tally_xy,
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_origin=None,
    plane_normal=[0, 0, 1],
    scale=LogNorm(),
    rotate_mesh=180,
    vmin=None,
    label="(n,Xa) per pulse",
    filename="mesh_tally_xy.png",
)

# plot.show()

plot = plot_regular_mesh_tally_with_geometry(
    tally=my_tally_xz,
    dagmc_file_or_trimesh_object="dagmc.h5m",
    plane_origin=[0,0.1,0],  # moves the slice 1mm into the 180 degree model to ensure geometry is sliced
    plane_normal=[0, 1, 0],
    rotate_geometry=90,
    scale=LogNorm(),
    vmin=None,
    label="(n,Xa)",
    filename="my_tally_xz.png",
)

# plot.show()

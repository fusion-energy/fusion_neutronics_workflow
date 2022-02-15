
# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
import os


my_reactor = paramak.BallReactor(
    inner_bore_radial_thickness=1,
    inboard_tf_leg_radial_thickness=30,
    center_column_shield_radial_thickness=60,
    divertor_radial_thickness=50,
    inner_plasma_gap_radial_thickness=30,
    plasma_gap_vertical_thickness=30,
    plasma_radial_thickness=300,
    outer_plasma_gap_radial_thickness=30,
    firstwall_radial_thickness=3,
    blanket_radial_thickness=100,
    blanket_rear_wall_radial_thickness=3,
    elongation=2.75,
    triangularity=0.5,
    number_of_tf_coils=16,
    rotation_angle=180
)

# exports the reactor shapes as a DAGMC h5m file which can be used as
# neutronics geometry by OpenMC
my_reactor.export_dagmc_h5m('dagmc.h5m')

# this converts the neutronics geometry h5m file into a vtk file for
# visualisation in Paraview or Visit
os.system('mbconvert dagmc.h5m dagmc.vtk')

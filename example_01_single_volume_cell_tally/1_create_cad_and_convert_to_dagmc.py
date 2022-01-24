# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
import os

my_shape = paramak.ExtrudeStraightShape(
    name='my_material',
    points=[(400, 100), (400, 200), (600, 200), (600, 100)],
    distance=180,
)

my_shape.export_dagmc_h5m('dagmc.h5m')

# this converts the neutronics geometry h5m file into a vtk file for
# visualisation in Paraview or Visit
os.system('mbconvert dagmc.h5m dagmc.vtk')

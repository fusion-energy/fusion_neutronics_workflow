import openmc
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import math
from openmc_dagmc_wrapper.utils import find_fusion_energy_per_reaction, write_3d_mesh_tally_to_vtk


def compute_volume_of_voxels(mesh):
    x = abs(mesh.lower_left[0] - mesh.upper_right[0])/mesh.dimension[0]
    y = abs(mesh.lower_left[1] - mesh.upper_right[1])/mesh.dimension[1]
    z = abs(mesh.lower_left[2] - mesh.upper_right[2])/mesh.dimension[2]
    volume = x*y*z
    return volume


statepoint_filename = "statepoint.60.h5"
statepoint = openmc.StatePoint(statepoint_filename)

fusion_power = 1e9
fusion_energy_per_reaction_j = find_fusion_energy_per_reaction('DT')
number_of_neutrons_per_second = fusion_power / fusion_energy_per_reaction_j

for tally in statepoint.tallies.values():
    if "_on_2D_mesh" in tally.name:
        my_slice = tally.get_slice(scores=tally.scores)
        tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
        mesh = tally_filter.mesh
        vol_cm3 = compute_volume_of_voxels(mesh)
        vol_m3 = vol_cm3*(1/100)**3
        shape = mesh.dimension.tolist()
        shape.remove(1)
        my_slice.mean.shape = shape[::-1]
        data = my_slice.mean/vol_m3*number_of_neutrons_per_second
        data = np.ma.masked_where(1e10 > data, data)

        fig = plt.subplot()
        im = fig.imshow(data, norm=LogNorm())
        plt.gca().invert_yaxis()
        plt.colorbar(im, label="He production (He/m3/s)")
        # plt.xlim(50, 400)
        # plt.ylim(100, 300)
        plt.ylim(100, 1150)
        plt.savefig('out.pdf', dpi=300)
        fig.clear()
    elif "_on_3D_mesh" in tally.name:
        print(f"processing {tally.name}")
        mesh_id = 1
        mesh = statepoint.meshes[mesh_id]

        vol_cm3 = compute_volume_of_voxels(mesh)
        vol_m3 = vol_cm3*(1/100)**3
        xs = np.linspace(
            mesh.lower_left[0], mesh.upper_right[0], mesh.dimension[0] + 1
        )
        ys = np.linspace(
            mesh.lower_left[1], mesh.upper_right[1], mesh.dimension[1] + 1
        )
        zs = np.linspace(
            mesh.lower_left[2], mesh.upper_right[2], mesh.dimension[2] + 1
        )
        tally = statepoint.get_tally(name=tally.name)

        data = tally.mean[:, 0, 0]/vol_m3*number_of_neutrons_per_second
        error = tally.std_dev[:, 0, 0]

        data = data.tolist()
        error = error.tolist()

        for content in [data, error]:
            for counter, i in enumerate(content):
                if math.isnan(i):
                    content[counter] = 0.0

        write_3d_mesh_tally_to_vtk(
            xs=xs,
            ys=ys,
            zs=zs,
            tally_label=tally.name,
            tally_data=data,
            error_data=error,
            outfile=tally.name.replace(
                "(",
                "").replace(
                ")",
                "").replace(
                ",",
                "-") +
            ".vtk",
        )
import numpy as np
import pandas as pd


def interpolame(in_df, field='"nh3_conc"', interp_factor=3):
    convert_dict = {"latitude":float, "longitude":float, field:float}
    z_df = z_df.astype(convert_dict)
    # Correct wraparound errors
    z_df.longitude[z_df.longitude > 180] -= 360.0
    z_df = z_df.sort_values(by=['longitude', 'latitude'])
    #
    # Check that the grid is uniform
    un_lon = len(z_df.longitude.unique())
    un_lat = len(z_df.latitude.unique())
    tot = len(z_df.longitude)

    assert tot == un_lon * un_lat, 'data grid is not uniform?!'
    assert un_lon == (z_df.latitude == z_df.latitude.iloc[0]).sum(), 'data grid is not uniform?!'
    assert un_lat == (z_df.longitude == z_df.longitude.iloc[0]).sum(), 'data grid is not uniform?!'

    data = z_df.to_numpy()

    long = data[:, 0]
    lat = data[:, 1]
    z = data[:, 2]

    extent = [min(long), max(long), min(lat), max(lat)]
    z_grid = np.reshape(z, [un_lon, -1])fit_points = [
        np.linspace(extent[0], extent[1], un_lon),
        np.linspace(extent[2], extent[3], un_lat),
    ]
    
    from scipy.interpolate import RegularGridInterpolator
    new_grid_sz = INTERPOLATION_FACTOR * np.array([un_lon, un_lat])
    ut, vt = np.meshgrid(
        np.linspace(extent[0], extent[1], new_grid_sz[0]),
        np.linspace(extent[2], extent[3], new_grid_sz[1]),
        indexing='ij')

    interp_points = np.array([ut.ravel(), vt.ravel()]).T
    interp = RegularGridInterpolator(fit_points, z_grid)
    z_grid_new = interp(interp_points, method='cubic').reshape(*new_grid_sz)
    
    return z_grid_new

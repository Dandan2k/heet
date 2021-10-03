# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Performs a regression algorithm that computes the best hypothesis for the
flooded area of a dam. The algorithm uses the GRanD database as a training set.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created: 09/07/2021
Last Modified: 09/07/2021

Author: Daniel-Alexandru Nistor
"""
# Import dam_data file to easily access the databases.
import dam_data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def surf_area_hyp(plot_hyp=False, save_theta=True):
    # We will use the GRanD database as a training set.
    training_set = dam_data.get_fltr_data("grand")
    # Create a shape tuple that has as many rows as the training set, but only
    # one column. This will simplify the code.
    shape = (len(training_set), 1)
    # Now, construct the design matrix. Note that the features are the logarithm
    # of the elevation and capacity.
    design_mtx = np.concatenate((np.ones(shape),
                                 np.log(training_set["Elevation"].reshape(shape)),
                                 np.log(training_set["Capacity"].reshape(shape))),
                                axis=1)

    # Also construct the target vector. Note that the target is the logarithm
    # of the area.
    target = np.log(training_set["Area"].reshape(shape))

    # Use the normal equation to find the best theta coefficients for the
    # hypothesis.
    theta = (np.linalg.pinv(design_mtx.transpose() @ design_mtx)
              @ design_mtx.transpose() @ target)

    # Plot the hypothesis against the training set if requested.
    if plot_hyp:
        # First plot the training set.
        fig, ax = plt.subplots(figsize=(9, 4), subplot_kw=dict(projection='3d'))
        ax.plot(design_mtx[:, 1].flatten(), design_mtx[:, 2].flatten(), target.flatten(),
                marker='o', linewidth=0, markersize=1, color='b')
        ax.set_xlabel("Log Elevation (masl)")
        ax.set_ylabel("Log Capacity (MW)")
        ax.set_zlabel("Log Area (sqkm)")
        fig.suptitle("Flooded Area Estimation - Hypothesis Visualisation")
        # Then plot the hypothesis.
        # This is the (rough) range of elevation values in the data.
        x = np.linspace(0, 8, 100)
        # This is the (rough) range of capacity values in the data.
        y = np.linspace(-3, 13, 100)
        # Create the meshes.
        xx, yy = np.meshgrid(x, y)
        # This is a matrix full of ones; we will use it to compute the hypothesis.
        ones = np.ones((np.shape(xx)))
        # Compute the hypothesis by reshaping the meshes into a new design
        # matrix and then taking its product with the theta vector. Basically,
        # we are doing vectorization. Since we have so little features, though,
        # we might try to simply write hyp = theta[0] * ones + theta[1] * xx + ...
        hyp = np.concatenate((ones.reshape(-1, 1), xx.reshape(-1, 1),
                              yy.reshape(-1, 1)), axis=1) @ theta
        # Plot the best-fit plane. Note that we need to reshape the hypothesis
        # vector once more.
        ax.plot_surface(xx, yy, hyp.reshape(np.shape(xx)), color='r', alpha=0.5)
        # Note that the plane will sometimes look as if it is above all scattered
        # points. It actually passes right through their middle -- this is a 
        # matplotlib issue.
        fig.show()

    # If the user wants to save the best fit parameters, create a text file
    # containing them, in the order theta[0], theta[1], etc. The elements are
    # on separate rows.
    if save_theta:
        np.savetxt("theta_values.txt", theta, fmt="%.5f")
    return theta

if __name__ == "__main__":
    surf_area_hyp(save_theta)

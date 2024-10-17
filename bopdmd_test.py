"""
This script tests BOPDMD on a complex signal.
The signal can be generated using the SignalGenerator class or loaded from a file.
"""

from pydmd import BOPDMD
from pydmd.preprocessing import hankel_preprocessing
from pydmd.plotter import plot_summary
from signal_generator import SignalGenerator
import matplotlib.pyplot as plt
from scipy.io import savemat, loadmat
import numpy as np

# Parameters
generate_data = False  # set to True to generate data, False to load data from file
save_data = True  # only relevant if generate_data=True
filename_save = "data/data_new.mat"  # path to save the data, if save_data=True
filename_load = "data/data.mat"  # path to load the data from, if generate_data=False
plot_results = True
apply_eig_constraints = False  # set to True to apply imaginary eigenvalue constraints

if generate_data:
    # Create a signal generator - currently generates a signal with three sinusoids and noise
    signal_generator = SignalGenerator(x_min=-5, x_max=5, t_max=60)
    signal_generator.add_sinusoid1(a=2, omega=0.5, k=1.5)
    signal_generator.add_sinusoid1(a=1, omega=2.5, k=1)
    signal_generator.add_sinusoid1(a=1, omega=5, k=-2)
    signal_generator.add_noise(random_seed=42)
    signal = signal_generator.signal
    t = signal_generator.t
    x = signal_generator.x

    if save_data:
        savemat(filename_save, {
            "signal": signal,
            "t": t,
            "x": x,
        })
else:
    try:
        print("Loading data...")
        data = loadmat(filename_load)
        signal = data["signal"]
        t = (data["t"]).squeeze()
        x = (data["x"]).squeeze()
    except FileNotFoundError:
        raise FileNotFoundError("Run the script with `generate_data=True` to generate data.")

# Apply BOPDMD without bagging
svd_rank = 6  # we have three components, so we need 6 DMD modes
delay = 2  # apply time-delay embedding

if not apply_eig_constraints:
    optdmd = BOPDMD(
        svd_rank=svd_rank,
        num_trials=0,
        use_proj=True,
        varpro_opts_dict={
            "verbose": True,
            },
    )
else:
    optdmd = BOPDMD(
        svd_rank=svd_rank,
        num_trials=0,
        use_proj=True,
        eig_constraints={"imag"},
        varpro_opts_dict={
            "verbose": True,
            },
    )

delay_optdmd = hankel_preprocessing(optdmd, d=delay)
t_delay = t[:-delay+1]
delay_optdmd.fit(signal.T, t=t_delay)

print("Eigenvalues:")
print(delay_optdmd.eigs)

print("Amplitudes:")
print(delay_optdmd.amplitudes)

if plot_results:
    plt.rcParams.update({'font.size': 4})
    plot_summary(delay_optdmd, x=x, d=delay, index_modes=[0, 2, 4])
    plt.show()

    # plot original vs reconstructed signal
    plt.rcParams.update({'font.size': 8})
    reconstructed_signal = delay_optdmd.forecast(t)
    reconstructed_signal = reconstructed_signal.real[:len(x), :].T
    levels = np.arange(-1.5, 1.6, 0.1)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax = ax.flatten()
    T, X = np.meshgrid(t, x)
    contour = ax[0].contourf(
        T, X, signal.T, levels=levels, cmap="bwr"
        )
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Space")
    ax[0].set_title("Original signal", fontsize=10)
    contour = ax[1].contourf(
        T, X, reconstructed_signal.T, levels=levels, cmap="bwr"
        )
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Space")
    ax[1].set_title("Reconstructed signal", fontsize=10)
    plt.colorbar(contour, ax=ax, orientation="vertical")
    plt.show()

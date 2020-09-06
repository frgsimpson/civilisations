import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from alien_app.utils import scaled_lognormal_pdf

N_POP_BINS = 20
MIN_POP = 100
MAX_POP = 1e18
MIN_MASS = 1e-2
MAX_MASS = 1e6


def make_population_figure(median_civ_population: float, variance: float) -> Figure:

    x_values = np.logspace(np.log10(MIN_POP), np.log10(MAX_POP), N_POP_BINS)
    y_values = scaled_lognormal_pdf(x_values, median_civ_population, variance)
    biased_median_population = np.exp(np.log(median_civ_population) + variance)
    biased_y_values = scaled_lognormal_pdf(x_values, biased_median_population, variance)

    fig, ax = plt.subplots(1, 2, figsize=(16, 4), sharex=True, sharey=True)
    widths = 0.9 * np.diff(x_values)
    ax[0].bar(x_values[:-1], y_values[:-1],  width=widths, align='edge')
    ax[1].bar(x_values[:-1], biased_y_values[:-1],  width=widths, align='edge')

    ax[0].set_xscale('log')
    ax[1].set_xscale('log')
    ax[0].set_xlabel('Populations of Civilisations')
    ax[1].set_xlabel('Populations where individuals belong')
    plt.xlim(x_values[0], x_values[-2])

    return fig


def make_mass_figure(median_species_mass: float, variance: float, correlation: float) -> Figure:
    """ Display the distribution of body masses. """

    x_values = np.logspace(np.log10(MIN_MASS), np.log10(MAX_MASS), N_POP_BINS)
    y_values = scaled_lognormal_pdf(x_values, median_species_mass, variance)

    biased_mean_population = np.exp(np.log(median_species_mass) + variance * correlation)
    biased_y_values = scaled_lognormal_pdf(x_values, biased_mean_population, variance)

    fig, ax = plt.subplots(1, 2, figsize=(16, 4), sharex=True, sharey=True)
    widths = 0.9 * np.diff(x_values)
    ax[0].bar(x_values[:-1], y_values[:-1],  width=widths, align='edge')
    ax[1].bar(x_values[:-1], biased_y_values[:-1],  width=widths, align='edge')

    ax[0].set_xscale('log')
    ax[1].set_xscale('log')
    ax[0].set_xlabel('Size of Alien Species (kg)')
    ax[1].set_xlabel('Size of Individual Aliens (kg)')
    plt.xlim(x_values[0], x_values[-2])

    return fig


if __name__ == '__main__':
    fig = make_population_figure(1e5, 2)
    plt.show()

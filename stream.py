""" An app which aims to illustrate the substantial difference between a typical alien civilisation and
the civilisation of the typical alien. """

import numpy as np
import streamlit as st

from alien_sampler import AlienSampler
from populations import make_population_figure, make_mass_figure
from utils import load_population_dict, load_mass_dict

N_SAMPLES = 7  # How many random samples to display

st.write("""
# Population Selection
Illustrating the difference between a typical alien civilisation and 
the civilisation of the typical alien.
Select a distribution of populations and body sizes.
""")

populations_dict = load_population_dict()
mass_dict = load_mass_dict()

pop_options = list(populations_dict.keys())
mass_options = list(mass_dict.keys())

populations = st.sidebar.select_slider("Typical population", options=pop_options, value='One million', key='pop')  # min max value step
log_population_variance = st.sidebar.slider(label="Spread in population of alien species", min_value=1., max_value=25., value=10., step=0.1)

mean_mass = st.sidebar.select_slider("Typical alien size (kg)", options=mass_options, value='Human (70 kg)', key='pop')  # min max value step
log_mass_variance = st.sidebar.slider(label="Spread in size of alien species", min_value=1., max_value=15., value=5., step=0.1)
mass_scaling = st.sidebar.slider(label="Mass-population scaling", min_value=0., max_value=1., value=0.5, step=0.01)

mass_correlation = -1. * mass_scaling  # Default negative correlation between population and body mass
# One issue is that a priori we should guess that mass scales inv with population.
# this isnt controlled by the correlation coefficient but how their variances are related in log space.

if st.button('Go'):
    population_mean = populations_dict[populations]
    pop_figure = make_population_figure(population_mean, log_population_variance)

    # Plot population chart
    st.write(pop_figure)

    # Plot mass chart
    mean_mass = mass_dict[mean_mass]
    log_mean_mass = np.log(mean_mass)
    mass_figure = make_mass_figure(mean_mass, log_mass_variance, mass_correlation)
    st.write(mass_figure)

    # Get random samples
    sampler = AlienSampler(np.log(population_mean), log_population_variance, log_mean_mass, log_mass_variance, mass_correlation)
    civ_dataframe = sampler.make_dataframe(n_samples=N_SAMPLES)
    individuals_dataframe = sampler.make_dataframe(n_samples=N_SAMPLES, biased=True)

    st.write("""
    # Examples of some random civilisations
    """)

    st.table(civ_dataframe)

    st.write("""
    # Examples of some civilisations where some random individuals live
    """)

    st.table(individuals_dataframe)

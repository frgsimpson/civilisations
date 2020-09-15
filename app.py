""" An app which aims to illustrate the substantial difference between a typical alien civilisation and
the civilisation of the typical alien. """

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from alien_plot import alien_array_plot
from alien_sampler import AlienSampler, BODY_MASS_STR
from populations import make_population_figure, make_mass_figure
from utils import load_population_dict, load_mass_dict

N_SAMPLES = 12  # How many random samples to display.
N_QUANTILES = 9  # How many quantiles to illustrate

st.write("""
# Cosmic Civilisations
Illustrating the difference between a typical alien civilisation and 
the civilisation of the typical alien.
""")

pd.options.display.float_format = '{:,.2g}'.format

populations_dict = load_population_dict()
mass_dict = load_mass_dict()

pop_options = list(populations_dict.keys())
mass_options = list(mass_dict.keys())

st.sidebar.write("Adjust the distribution of populations and body sizes.")
st.sidebar.write("Population settings")

populations = st.sidebar.select_slider("Typical population", options=pop_options, value='One million', key='pop')  # min max value step
log_population_std = st.sidebar.slider(label="Spread in population of alien species", min_value=0.1, max_value=5., value=3., step=0.1)

st.sidebar.write("Mass settings")

mean_mass = st.sidebar.select_slider("Typical alien size (kg)", options=mass_options, value='Human (70 kg)', key='pop') # min max value step
log_mass_std = st.sidebar.slider(label="Spread in size of alien species", min_value=0.1, max_value=4., value=2.0, step=0.1)
mass_scaling = st.sidebar.slider(label="Mass-population scaling", min_value=0., max_value=1., value=0.4, step=0.01)

mass_correlation = -1. * mass_scaling  # Default negative correlation between population and body mass
# One issue is that a priori we should guess that mass scales inv with population.
# this isnt controlled by the correlation coefficient but how their variances are related in log space.

# Galaxy image
image = Image.open('galaxy.jpg')
st.image(image, use_column_width=True)

if st.button('Go'):
    log_mass_variance = log_mass_std ** 2
    log_population_variance = log_population_std ** 2
    population_mean = populations_dict[populations]
    mean_mass = mass_dict[mean_mass]
    log_mean_mass = np.log(mean_mass)

    # Get random samples
    sampler = AlienSampler(np.log(population_mean), log_population_variance, log_mean_mass, log_mass_variance, mass_correlation)
    civ_dataframe = sampler.make_dataframe(n_samples=N_SAMPLES)
    individuals_dataframe = sampler.make_dataframe(n_samples=N_SAMPLES, biased=True)

    mass_index = 1
    alien_masses = sampler.draw_spaced_quantiles(n_samples=N_QUANTILES, index=mass_index, biased=True) # individuals_dataframe[BODY_MASS_STR]
    alien_heights = alien_masses ** 0.3333
    species_masses = sampler.draw_spaced_quantiles(n_samples=N_QUANTILES, index=mass_index)  # civ_dataframe[BODY_MASS_STR]
    species_heights = species_masses ** 0.3333

    alien_array_figure = alien_array_plot(species_heights, alien_heights, spacing=2.)

    st.markdown('The <span style="color: red;">size of species (red)</span> compared to the size of individuals (black).', unsafe_allow_html=True)

    st.pyplot(alien_array_figure)

    pop_figure = make_population_figure(population_mean, log_population_variance)
    mass_figure = make_mass_figure(mean_mass, log_mass_variance, mass_correlation)

    st.write("""
    # Examples of alien civilisations
    """)

    st.table(civ_dataframe)

    st.write("""
    # Examples of individual aliens
    """)

    st.table(individuals_dataframe)

    # Plot population chart
    st.write(pop_figure)

    # Plot mass chart
    st.write(mass_figure)

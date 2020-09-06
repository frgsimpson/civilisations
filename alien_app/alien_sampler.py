""" Properties of alien civilisations based upon a multivariate gaussian distribution. """

import numpy as np
import pandas as pd


class AlienSampler:
    """ Holds information on the distribution of aliens in the universe, allowing random samples to be drawn. """
    def __init__(self, log_population_mean: float, log_population_variance, log_mass_mean, log_mass_variance,
                 mass_correlation):
        """ Sampler describes the distribution of alien civilisations. Currently the only properties are population
        body mass and land area. """

        self.properties = ['Population', 'Body mass (kg)', 'Area']
        self.n_properties = len(self.properties)

        self.log_population_mean = log_population_mean
        self.log_population_variance = log_population_variance
        self.log_mass_mean = log_mass_mean
        self.log_indices = [0, 1, 2]  # which properties are represented by their log
        self.log_mass_variance = log_mass_variance
        self.log_area_mean = 10  # todo customise
        self.log_area_variance = 1.
        self.mass_correlation = mass_correlation
        self.area_correlation = 0.2

    def get_means(self):
        return [self.log_population_mean, self.log_mass_mean, self.log_area_mean]

    def get_covariance(self):  # todo add area correlation

        cov = np.zeros((self.n_properties, self.n_properties))

        cov[0, 0] = self.log_population_variance
        cov[1, 1] = self.log_mass_variance
        cov[2, 2] = self.log_area_variance

        cov[0, 1] = self.mass_correlation * np.sqrt(self.log_population_variance * self.log_mass_variance)
        cov[1, 0] = cov[0, 1]

        return cov

    def make_dataframe(self, n_samples: int,  biased=False):

        samples = self.draw_samples(n_samples, biased)
        df = pd.DataFrame(samples, columns=self.properties)

        return df

    def draw_samples(self, n_samples: int, biased=False):
        """ Provide random samples of the properties of civilisations.

         biased - Provide random samples of individuals, returning the properties of their civilisations
         """

        means = self.get_means()
        cov = self.get_covariance()

        if biased:
            # Log population's mean is shifted by its variance
            means[0] += cov[0, 0]
            means[1] += cov[1, 1] * self.mass_correlation
            means[2] += cov[2, 2] * self.area_correlation

        samples = np.random.multivariate_normal(means, cov, n_samples)

        for index in self.log_indices:
            samples[:, index] = np.exp(samples[:, index])

        return samples.astype(np.int64)


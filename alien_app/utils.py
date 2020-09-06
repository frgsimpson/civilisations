import numpy as np


def lognormal_pdf(x, mu, sig):
    gauss = normal_pdf(np.log(x), mu, sig)
    return gauss / x


def scaled_lognormal_pdf(x, mu, variance):
    """
    The lognormal pdf as viewed in log x, i.e. standard normal distribution
    """
    return normal_pdf(np.log(x), np.log(mu), np.sqrt(variance))


def normal_pdf(x, mu, sig):
    c = 1 / np.sqrt(2 * np.pi * sig ** 2)
    return c * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def load_population_dict() -> dict:
    number = {'One': 1,
              'Ten': 10,
              'Hundred':  100,
              'One thousand': 1_000,
              'Ten thousand': 10_000,
              'Hundred Thousand': 100_000,
              'One million': 1_000_000,
              'Ten Million': 10_000_000,
              'Hundred Million': 100_000_000,
              'One Billion': 1_000_000_000,
              'Ten Billion': 10_000_000_000,
              'Hundred Billion': 100_000_000_000,
              'One Trillion': 1_000_000_000_000,
              'Ten Trillion': 10_000_000_000_000,
              }
    return number


def load_mass_dict() -> dict:
    mass = {'Tiny (1 kg)': 1,
              'Small (10 kg)': 10,
              'Human (70 kg)':  70,
              'Large (300 kg)': 1_000,
              'Very large (5,000 kg)': 10_000,
              'Giant (100,000 kg)': 100_000,
              }
    return mass

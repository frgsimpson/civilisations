""" Make plot showing a sequence of scaled aliens. """

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

ALIEN_FILENAME = './assets/human.png'
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 3


def alien_array_plot(heights, secondary_heights, images=None, spacing: float = 0.) -> Figure:
    """
    Generate a figure demonstrating the size distribution of aliens and alien species.
    """
    fig, ax = plt.subplots(1, 1, figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    prev_image_ends = 0

    if images is None:
        alien_image = plt.imread(ALIEN_FILENAME, format='RGBA').copy()
        images = [alien_image for _ in heights]
        alt_img = np.copy(alien_image)

        max_val = np.max(alt_img.flatten())
        if max_val > 10:
            white_bits = alt_img[:, :, 1] > 200
            alt_img[:, :, 0] = 230  # Set red channel high everywhere
        else:
            white_bits = alt_img[:, :, 1] == 1.
            alt_img[:, :, 0] = 0.9  # Set red channel high everywhere

        alien_image[:, :, -1][white_bits] = 0.  # Invoke transparant background for background image
        alt_img[:, :, -1][white_bits] = 0.  # Invoke transparant background for foreground image

        alt_images = [alt_img for _ in heights]

    centres = []
    for i, (height, img, alt_img) in enumerate(zip(heights, images, alt_images)):
        AR = img.shape[1] / img.shape[0]

        width = height * AR
        left = prev_image_ends
        right = left + width
        centre = (left + right) / 2
        centres.append(centre)

        ax.imshow(img, extent=[left, right, 0, height])
        alt_height = secondary_heights[i]
        alt_width = alt_height * AR
        alt_left = centre - alt_width / 2
        alt_right = centre + alt_width / 2

        ax.imshow(alt_img, extent=[alt_left, alt_right, 0, alt_height])

        prev_image_ends += spacing

    x_centres = np.stack(centres)
    ax.set_xticks(x_centres)
    ax.set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%'])
    ax.get_yaxis().set_visible(False)

    # Set x,y limits on plot window
    plt.xlim(0, right)

    median_species_height = heights[4]
    plt.ylim(0, median_species_height * 1.5)

    plt.box(on=None)
    return fig

from argparse import ArgumentParser
from astropy.io import fits
from matplotlib.animation import FuncAnimation
from fact.plotting import camera
import numpy as np
import matplotlib.pyplot as plt


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('eventnum', type=int)
parser.add_argument('outputfile')
parser.add_argument(
    '--first', dest='first', type=int, default=20,
    help='first slice to plot',
)
parser.add_argument(
    '--last', dest='last', type=int, default=200,
    help='last slice to plot',
)


def main():
    args = parser.parse_args()

    with fits.open(args.inputfile) as f:
        data = f[1].data[args.eventnum]['DataCalibrated']

    img = data.reshape((1440, 300))
    img = img[:, args.first:args.last]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    vmin = np.nanpercentile(img, 1)
    vmax = np.nanpercentile(img, 99)
    c = camera(img[:, 0], cmap='inferno', vmin=vmin, vmax=vmax)
    template = '$t = {: 3.1f}\,\mathrm{{ns}}$'
    t = plt.text(120, 189, template.format(0), size=30, va='top')

    def update(i):
        c.set_array(img[:, i])
        t.set_text(template.format(i / 2))
        return c, t

    ani = FuncAnimation(fig, update, np.arange(0, img.shape[1]), interval=100, blit=True)

    ani.save(args.outputfile, writer='imagemagick', dpi=40)


if __name__ == '__main__':
    main()

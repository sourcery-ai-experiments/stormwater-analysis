import math
import logging
import matplotlib.pyplot as plt
import pandas as pd
from numpy import sin, cos, pi, linspace
from pipes.round import (max_filling, max_velocity, min_velocity)

logger = logging.getLogger(__name__)


def validate_filling(filling: float, diameter: float) -> bool:
    """
    Check that the maximum filling is not exceeded.

    Args:
        filling (int, float): pipe filling height [m].
        diameter (int, float): pipe diameter [m].

    Return:
        bool: given filling value is lower than the maximum filling.
    """
    return filling <= max_filling(diameter)


def validate_max_velocity(velocity: float) -> bool:
    """
    Check that the maximum velocity is not exceeded.

    Args:
        velocity (int, float): flow velocity in the sewer [m/s].

    Return:
        bool: given velocity value is lower than the maximum velocity.
    """
    return velocity <= max_velocity()


def validate_min_velocity(velocity: float) -> bool:
    """
    Check that the minimum velocity is not exceeded.
    For hydraulic calculations of sewers and rainwater collectors,
    it is recommended to adopt a self-cleaning velocity
    of not less than 0.7 m - s-1 to prevent solids from settling at the bottom of the sewer.
    source: PN-EN 752:2008 Zewnętrzne systemy kanalizacyjne - in polish

    Args:
        velocity (int, float): flow velocity in the sewer [m/s].

    Return:
        bool: given velocity value is higher than the maximum velocity.
    """
    return velocity >= min_velocity()


def draw_pipe_section(h, d, max_filling=None):
    """
    Plot a pipe section with a given diameter and filling height.

    Args:
        h (int, flow): height of the water level in the pipe
        d (int, flow): diameter of the pipe
        max_filling (int, flow): The maximum filling of the pipe. If the pipe is filled above this level, the wetted part of the pipe
            will be drawn in red
    """
    if max_filling is None:
        max_filling = d
    if validate_filling(h, d):
        radius = d / 2
        # draw center point  - 0, 0
        plt.plot(0, 0, color="black", marker="o")
        plt.gca().annotate(
            "O (0, 0)",
            xy=(0 + radius / 10, 0 + radius / 10),
            xycoords="data",
            fontsize=12,
        )
        plt.xlim(-radius - 0.05, radius + 0.05)
        plt.ylim(-radius, radius + 0.07)
        plt.gca().set_aspect("equal")

        # draw circle
        angels = linspace(0 * pi, 2 * pi, 100)
        xs = radius * cos(angels)
        ys = radius * sin(angels)
        # add circle
        plt.plot(xs, ys, color="brown", label=f"Pipe: DN {d} [m]")

        # draw diameter
        plt.plot(radius, 0, marker="o", color="blue")
        plt.plot(-radius, 0, marker="o", color="blue")
        plt.plot([radius, -radius], [0, 0])
        # annotation to diameter
        plt.gca().annotate(
            f"Diameter={d}", xy=(radius / 8, -radius / 5), xycoords="data", fontsize=12
        )

        # draw level of water
        plt.plot(0, -radius, marker="o", color="purple")
        plt.plot(0, h - radius, marker="o", color="purple")
        plt.plot(
            [0, 0],
            [-radius, h - radius],
            color="purple",
            label=f"Pipe filling height: {h} [m]",
        )
        plt.gca().annotate(
            f"Water lvl={h}",
            xy=(radius / 2, h - radius + 0.01),
            xycoords="data",
            fontsize=12,
        )

        # Draw arc as created by water level
        chord = math.sqrt((radius**2 - ((h - radius) ** 2))) * 2
        alpha = math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))

        if h > max_filling:
            color = "red"
        else:
            color = "blue"
        # Create arc
        if h <= radius:
            diff = math.radians(180) - alpha
            arc_angles = linspace(diff / 2, alpha + diff / 2, 20)
        else:
            diff = math.radians(180) - alpha
            arc_angles = linspace(-diff / 2, alpha + diff + diff / 2, 100)
        arc_xs = radius * cos(arc_angles)
        arc_ys = radius * sin(arc_angles)
        plt.plot(arc_xs, -arc_ys, color=color, lw=3)
        plt.plot(
            [-arc_xs[0], -arc_xs[-1]],
            [-arc_ys[0], -arc_ys[-1]],
            marker="o",
            color=color,
            lw=3,
            label=f"Wetted part of pipe: {calc_f(h, d):.2f} [m2]",
        )
        plt.grid(True)
        plt.legend(loc="upper left")
        plt.show()
    else:
        logger.info(f"h cannot be greater than d.")

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

import math
import logging
import matplotlib.pyplot as plt
import pandas as pd
from numpy import sin, cos, pi, linspace

logger = logging.getLogger(__name__)


def max_filling(diameter: float) -> float:
    """
    > Calculates the maximum filling of a rainwater drain with a circular cross-section.

    According to a methodology based on the Colebrook-White formula, the total
    capacity of the channel (100%), i.e., with total cross-sectional filling
    (100%), is already achieved at a relative filling of 4/D = 0.827 - in circular pipes,
    Kotowski, A., Kaźmierczak, B., & Dancewicz, A. (2010).
    Modelowanie opadów do wymiarowania kanalizacji.
    Polska Akademia Nauk. Instytut Podstawowych Problemów Techniki.

    Args:
        diameter (int, float): the diameter of the rainwater pipe [m].

    Return:
        maximum filling (float): he maximum pipe filling [m].
    """
    if isinstance(diameter, (int, float)):
        if 0.2 <= diameter <= 2.0:
            return 0.827 * diameter
        else:
            raise ValueError("Invalid diameter value.")
    else:
        raise TypeError("Diameter must be an int or float")


def max_velocity():
    """
    Maximum sewage flow velocity in the sewer [m/s].

    Return:
         velocity (int): maximum sewage flow velocity in pipe [m].
    """

    return 3


def min_velocity():
    """
    Minimum sewage flow velocity in the sewer [m/s].

    Return:
         velocity (int): minimum sewage flow velocity in pipe [m].
    """

    return 0.7


def calc_f(filling: float, diameter: float) -> float:
    """
    Calculate the cross-sectional area of a pipe.
    The cross-sectional area through which the wastewater flows, active cross-section f,
    characterized by the filling h and the diameter of the pipe D.
    source: Biedugnis S., “Metody informatyczne w wodociągach i kanalizacji”,
    Oficyna Wydawnicza Politechniki Warszawskiej, Warszawa 1998. - in polish.

    Args:
        filling (int, float): pipe filling height [m]
        diameter (int, float): pipe diameter [m]

    Return:
        area (int, float): cross-sectional area of the wetted part of the pipe [m2]
    """
    radius = diameter / 2
    chord = math.sqrt((radius**2 - ((filling - radius) ** 2))) * 2
    alpha = math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))
    if filling > radius:
        return pi * radius**2 - (1 / 2 * (alpha - math.sin(alpha)) * radius**2)
    elif filling == radius:
        return pi * radius**2 / 2
    elif filling == diameter:
        return pi * radius**2
    else:
        return 1 / 2 * (alpha - math.sin(alpha)) * radius**2


def calc_u(filling: float, diameter: float) -> float:
    """
    Calculate the circumference of a wetted part of pipe.
    source: Biedugnis S., “Metody informatyczne w wodociągach i kanalizacji”,
    Oficyna Wydawnicza Politechniki Warszawskiej, Warszawa 1998. - in polish.

    Args:
        filling (int, float): pipe filling height [m]
        diameter (int, float): pipe diameter [m]

    Return:
        circumference (int, float): circumference of a wetted part of pipe
    """
    radius = diameter / 2
    chord = math.sqrt((radius**2 - (filling - radius) ** 2)) * 2
    alpha = math.degrees(
        math.acos((radius**2 + radius**2 - chord**2) / (2 * radius**2))
    )
    if filling > radius:
        return 2 * math.pi * radius - (alpha / 360 * 2 * math.pi * radius)
    return alpha / 360 * 2 * math.pi * radius


def calc_rh(filling: float, diameter: float) -> float:
    """
    Calculate the hydraulic radius Rh, i.e. the ratio of the cross-section f
    to the contact length of the sewage with the sewer wall, called the wetted circuit U.
    source: Biedugnis S., “Metody informatyczne w wodociągach i kanalizacji”,
    Oficyna Wydawnicza Politechniki Warszawskiej, Warszawa 1998. - in polish.

    Args:
        filling (int, float): pipe filling height [m]
        diameter (int, float): pipe diameter [m]

    Return:
        Rh (int, float): hydraulic radius [m]
    """
    try:
        return calc_f(filling, diameter) / calc_u(filling, diameter)
    except ZeroDivisionError:
        return 0


def min_slope(filling: float, diameter: float) -> float:
    """
    Get the minimal slope for sewer pipe.
    If the pipe  filling is greater than 0.3,
    then the minimum slope is 1/d, otherwise it's 0.25/rh

    source: Suligowski : Samooczyszczanie przewodów kanalizacyjnych. Instal 2010, nr 2, s. 48-53. - in polish
    source: https://seidel-przywecki.eu/2021/06/04/obliczenia-hydraulicznych-kanalow-sciekowych-i-deszczowych/

    Args:
        filling (int, float): pipe filling height [m]
        diameter (int, float): pipe diameter [m]

    Return:
        slope (int, float): The minimum slope of the channel [‰]
    """
    return 0.612 * (10**-3) * ((diameter / 4) / calc_rh(filling, diameter)) * (1 / diameter)

import logging

import numpy
import swisseph as swe

from jyotisha.panchangam.temporal.body import Graha

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)


class Ayanamsha(object):
    CHITRA_AT_180 = "CHITRA_AT_180"
    
    def __init__(self, ayanamsha_id):
        self.ayanamsha_id = ayanamsha_id
    
    def get_offset(self, jd):
        if self.ayanamsha_id == Ayanamsha.CHITRA_AT_180:
            # TODO: The below fails due to https://github.com/astrorigin/pyswisseph/issues/35
            from jyotisha.panchangam.temporal import body
            return (body.get_star_longitude(star="Spica", jd=jd)-180)
            # swe.set_sid_mode(swe.SIDM_LAHIRI)
            # return swe.get_ayanamsa_ut(jd)
        raise Exception("Bad ayamasha_id")


class NakshatraDivision(object):
  """Nakshatra division at a certain time, according to a certain ayanaamsha."""

  def __init__(self, julday, ayanamsha_id=Ayanamsha.CHITRA_AT_180):
    self.ayanamsha_id = ayanamsha_id
    
    self.set_time(julday=julday)

  # noinspection PyAttributeOutsideInit
  def set_time(self, julday):
    self.julday = julday
    self.right_boundaries = ((numpy.arange(27) + 1) * (360.0 / 27.0) + Ayanamsha(self.ayanamsha_id).get_offset(julday)) % 360

  def get_nakshatra(self, body, julday=None):
    if julday is not None:
      self.set_time(julday=julday)
    logging.debug(Ayanamsha(self.ayanamsha_id).get_offset(self.julday))
    return ((Graha(body).get_longitude(self.julday) - Ayanamsha(self.ayanamsha_id).get_offset(self.julday)) % 360) / (360.0 / 27.0)

  def __str__(self):
    return str(self.__dict__)

  def get_equatorial_boundary_coordinates(self):
    """Get equatorial coordinates for the points where the ecliptic nakShatra boundary longitude intersects the ecliptic."""
    equatorial_boundary_coordinates = [ecliptic_to_equatorial(longitude=longitude, latitude=0) for longitude in self.right_boundaries]
    return equatorial_boundary_coordinates

  def get_stellarium_nakshatra_boundaries(self):
    equatorial_boundary_coordinates_with_ra = self.get_equatorial_boundary_coordinates()
    ecliptic_north_pole_with_ra = ecliptic_to_equatorial(longitude=20, latitude=90)
    # logging.debug(ecliptic_north_pole_with_ra)
    ecliptic_south_pole_with_ra = ecliptic_to_equatorial(longitude=20, latitude=-90)
    # logging.debug(ecliptic_south_pole_with_ra)
    for index, (boundary_ra, boundary_declination) in enumerate(equatorial_boundary_coordinates_with_ra):
      print(
        '3 %(north_pole_ra)f %(north_pole_dec)f %(boundary_ra)f %(boundary_declination)f %(south_pole_ra)f %(south_pole_dec)f 2 N%(sector_id_1)02d N%(sector_id_2)02d' % dict(
          north_pole_ra=ecliptic_north_pole_with_ra[0],
          north_pole_dec=ecliptic_north_pole_with_ra[1],
          boundary_ra=boundary_ra,
          boundary_declination=boundary_declination,
          south_pole_ra=ecliptic_south_pole_with_ra[0],
          south_pole_dec=ecliptic_south_pole_with_ra[1],
          sector_id_1=(index % 27 + 1),
          sector_id_2=((index + 1) % 27 + 1)
        ))


def get_nirayana_sun_lon(jd, offset=0, debug=False):
    """Returns the nirayana longitude of the sun

      Args:
        float jd: The Julian Day at which the angam is to be computed

      Returns:
        float longitude

      Examples:
    """
    lsun = (Graha(Graha.SUN).get_longitude(jd)) % 360

    if debug:
        print('## get_angam_float(): lsun (nirayana) =', lsun)

    if offset + 360 == 0 and lsun < 30:
        # Angam 1 -- needs different treatment, because of 'discontinuity'
        return lsun
    else:
        return lsun + offset



def longitudeToRightAscension(longitude):
    return (360 - longitude) / 360 * 24


def ecliptic_to_equatorial(longitude, latitude):
    coordinates = swe.cotrans(lon=longitude, lat=latitude, dist=9999999, obliquity=23.437404)
    # swe.cotrans returns the right ascension longitude in degrees, rather than hours.
    return (
        longitudeToRightAscension(coordinates[0]), coordinates[1])


if __name__ == '__main__':
    # lahiri_nakshatra_division = NakshatraDivision(julday=temporal.utc_to_jd(year=2017, month=8, day=19, hour=11, minutes=10, seconds=0, flag=1)[0])
    import temporal
    lahiri_nakshatra_division = NakshatraDivision(
        julday=temporal.utc_gregorian_to_jd(year=1982, month=2, day=19, fractional_hour=11, minutes=10, seconds=0, flag=1)[0])
    logging.info(lahiri_nakshatra_division.get_nakshatra(body=Graha.MOON))
    # logging.info(lahiri_nakshatra_division)
    lahiri_nakshatra_division.get_stellarium_nakshatra_boundaries()

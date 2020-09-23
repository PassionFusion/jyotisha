import logging
import math
import os

from indic_transliteration import xsanscript as sanscript

from jyotisha.panchangam.spatio_temporal import City, annual
# from jyotisha.panchangam import scripts
# from jyotisha.panchangam.spatio_temporal import annual
from jyotisha.panchangam.temporal import zodiac
from sanskrit_data.schema.common import JsonObject

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s: %(asctime)s {%(filename)s:%(lineno)d}: %(message)s "
)

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


def test_panchanga_chennai_18(caplog):
  caplog.set_level(logging.INFO)
  panchangam_expected_chennai_18 = JsonObject.read_from_file(filename=os.path.join(TEST_DATA_PATH, 'Chennai-2018.json'))
  panchangam_expected_chennai_18.update_festival_details()
  city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
  panchangam = annual.get_panchaanga(city=city, year=2018, script=sanscript.DEVANAGARI,
                                     ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                     allow_precomputed=False)

  if panchangam.to_json_map(floating_point_precision=4) != panchangam_expected_chennai_18.to_json_map(
      floating_point_precision=4):
    panchangam.dump_to_file(filename=os.path.join(TEST_DATA_PATH, 'Chennai-2018-actual.json.local'),
                            floating_point_precision=4, sort_keys=False)
    panchangam_expected_chennai_18.dump_to_file(
      filename=os.path.join(TEST_DATA_PATH, 'Chennai-2018-expected.json.local'), floating_point_precision=4,
      sort_keys=False)
  assert panchangam.to_json_map(floating_point_precision=4) == panchangam_expected_chennai_18.to_json_map(
    floating_point_precision=4)


def test_panchanga_chennai_19():
  panchangam_expected_chennai_19 = JsonObject.read_from_file(filename=os.path.join(TEST_DATA_PATH, 'Chennai-2019.json'))
  panchangam_expected_chennai_19.update_festival_details()
  city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
  panchangam = annual.get_panchaanga(city=city, year=2019, script=sanscript.DEVANAGARI,
                                     ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                     allow_precomputed=False)

  if panchangam.to_json_map(floating_point_precision=4) != panchangam_expected_chennai_19.to_json_map(
      floating_point_precision=4):
    panchangam.dump_to_file(filename=os.path.join(TEST_DATA_PATH, 'Chennai-2019-actual.json.local'),
                            floating_point_precision=4)
    panchangam_expected_chennai_19.dump_to_file(
      filename=os.path.join(TEST_DATA_PATH, 'Chennai-2019-expected.json.local'), floating_point_precision=4)
  assert panchangam.to_json_map(floating_point_precision=4) == panchangam_expected_chennai_19.to_json_map(
    floating_point_precision=4)


def test_panchanga_orinda():
  panchangam_expected_orinda_19 = JsonObject.read_from_file(filename=os.path.join(TEST_DATA_PATH, 'Orinda-2019.json'))
  panchangam_expected_orinda_19.update_festival_details()
  city = City('Orinda', '37:51:38', '-122:10:59', 'America/Los_Angeles')
  panchangam = annual.get_panchaanga(city=city, year=2019, script=sanscript.DEVANAGARI,
                                     ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                     allow_precomputed=False)

  if panchangam.to_json_map(floating_point_precision=4) != panchangam_expected_orinda_19.to_json_map(
      floating_point_precision=4):
    panchangam.dump_to_file(filename=os.path.join(TEST_DATA_PATH, 'Orinda-2019-actual.json.local'),
                            floating_point_precision=4)
    panchangam_expected_orinda_19.dump_to_file(filename=os.path.join(TEST_DATA_PATH, 'Orinda-2019-expected.json.local'),
                                               floating_point_precision=4)
  assert panchangam.to_json_map(floating_point_precision=4) == panchangam_expected_orinda_19.to_json_map(
    floating_point_precision=4)


def test_adhika_maasa_computations_2009():
  city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
  panchangam_2009 = annual.get_panchaanga(city=city, year=2009, script=sanscript.DEVANAGARI,
                                          ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                          allow_precomputed=False)
  expected_lunar_months_2009 = [7] + [8] * 29 + [9] * 30 + [10] * 15
  assert expected_lunar_months_2009 == panchangam_2009.lunar_month[291:366]


def test_adhika_maasa_computations_2010():
  city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
  panchangam_2010 = annual.get_panchaanga(city=city, year=2010, script=sanscript.DEVANAGARI,
                                          ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                          allow_precomputed=False)
  expected_lunar_months_2010 = [10] * 15 + [11] * 30 + [12] * 29 + [1] * 30 + [1.5] * 30 + [2] * 29 + [3]
  assert expected_lunar_months_2010 == panchangam_2010.lunar_month[1:165]


def test_adhika_maasa_computations_2018():
  city = City('Chennai', "13:05:24", "80:16:12", "Asia/Calcutta")
  panchangam_2018 = annual.get_panchaanga(city=city, year=2018, script=sanscript.DEVANAGARI,
                                          ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                          allow_precomputed=False)
  expected_lunar_months_2018 = [2] + [2.5] * 29 + [3] * 30 + [4]
  assert expected_lunar_months_2018 == panchangam_2018.lunar_month[135:196]


def test_orinda_ca_dst_2019():
  city = City('Orinda', '37:51:38', '-122:10:59', 'America/Los_Angeles')
  panchangam = annual.get_panchaanga(city=city, year=2019, script=sanscript.DEVANAGARI,
                                     ayanamsha_id=zodiac.Ayanamsha.CHITRA_AT_180, compute_lagnas=False,
                                     allow_precomputed=False)
  # March 10 is the 69th day of the year (70th in leap years) in the Gregorian calendar.
  # Sunrise on that day is around 7:27 AM according to Google, which is JD 2458553.14375 according to https://ssd.jpl.nasa.gov/tc.cgi#top .
  # We use the index 70 below as the annual panchanga object seems to use the index d + 1.
  assert round(panchangam.jd_sunrise[70], ndigits=4) == round(2458554.104348237, ndigits=4)  # 2019-Mar-10 07:30:15.68

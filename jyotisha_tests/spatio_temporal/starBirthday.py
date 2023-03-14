import copy
import logging
import os

import jyotisha.panchaanga.temporal
from sanskrit_data import testing
from timebudget import timebudget
from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.spatio_temporal.daily import DailyPanchaanga
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha_tests.spatio_temporal import chennai
from datetime import datetime
from jyotisha.panchaanga.writer.tex.day_details import _get_relative_nadikas
from pytz import timezone as tz
from indic_transliteration import sanscript
from jyotisha.panchaanga.temporal import names, time
from jd_date_utils import calculate_jd,julian_date_to_datetime 
from jyotisha.panchaanga.temporal import zodiac
from jyotisha.panchaanga.temporal.zodiac import NakshatraDivision,Ayanamsha

scripts = [sanscript.DEVANAGARI]
languages = ["sa"]
time_format="hh:mm"

## Narayanan IST
# city=City('Chennai', '13:05:24', '80:16:12', 'Asia/Calcutta')
# yyyy = 1984
# mon = 5
# dd = 5
# hh = 1
# mm = 57
# ss = 0

## Akshara IST
# city=City('Chennai', '13:05:24', '80:16:12', 'Asia/Calcutta')
# yyyy = 2022
# mon = 4
# dd = 1
# hh = 1
# mm = 57
# ss = 0

## Swara EST
# city = City('Brussels', '50.850346', '4.351721', 'Europe/Brussels')
# yyyy = 2017
# mon = 3
# dd = 24
# hh = 1
# mm = 9
# ss = 0


## Swara EST
city = City('Brussels', '50.850346', '4.351721', 'Europe/Brussels')
yyyy = 2023
mon = 4
dd = 14
hh = 1
mm = 9
ss = 0

# dt = datetime(yyyy, mon, dd, hh, mm, ss)

# birth_jd = calculate_jd(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, 2)

# # Convert the floating-point Julian day to an integer
# birth_jd = int(birth_jd + 0.5)

# print(f"The Julian day for {dt} is {birth_jd}.")

# nd = NakshatraDivision(birth_jd, Ayanamsha.CHITRA_AT_180).get_nakshatra()

# print(f"The nakshatra for {dt} is {nd.get_name()}.")


# nd_name = NakshatraDivision(birth_jd, Ayanamsha.CHITRA_AT_180).get_nakshatra().get_name()

# nd_tamil = names.translate_or_transliterate(text=nd_name,script=sanscript.TAMIL)

# print (f'NakshatraDivision = {nd} - {nd_name} - {nd_tamil}')

def get_nakshatra_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga=None, include_early_end_angas=False):
  jd = daily_panchaanga.julian_day_start
  nakshatra_data_str = ''
  for iNakshatra, nakshatra_span in enumerate(daily_panchaanga.sunrise_day_angas.nakshatras_with_ends):
    (nakshatra_ID, nakshatra_end_jd) = (nakshatra_span.anga.index, nakshatra_span.jd_end)
    if nakshatra_data_str != '':
      nakshatra_data_str += 'hspace{1ex}'
    
    nakshatra_dev = names.NAMES['NAKSHATRA_NAMES']['sa'][scripts[0]][nakshatra_ID]
    nakshatra_eng = names.translate_or_transliterate(text=nakshatra_dev, source_script=sanscript.DEVANAGARI, script=sanscript.HK)
    nakshatra = names.translate_or_transliterate(text=nakshatra_dev,source_script=sanscript.DEVANAGARI, script=sanscript.TAMIL)
    if nakshatra_end_jd is None:
      if iNakshatra == 0:
        nakshatra_data_str = '%sfullanga{%s}' % (nakshatra_data_str, nakshatra)
    else:
      nakshatra_data_str = '%sanga{%s-%s-%s}{time{%s}{%s}}' % \
                           (nakshatra_data_str, nakshatra_eng, nakshatra_dev, nakshatra,
                            # time.Hour(24 * (nakshatra_end_jd - daily_panchaanga.jd_sunrise)).to_string(format='gg-pp'),
                            _get_relative_nadikas(nakshatra_end_jd, daily_panchaanga),
                            time.Hour(24 * (nakshatra_end_jd - jd)).to_string(format=time_format))
    if iNakshatra == 2:
      nakshatra_data_str += 'avamA{}'

  if include_early_end_angas:
    if previous_day_panchaanga is None:
      logging.error('Unable to include early end angas, as previous_day_panchaanga is not supplied!')
    if len(previous_day_panchaanga.sunrise_day_angas.nakshatras_with_ends) > 1:
      nakshatra_span = previous_day_panchaanga.sunrise_day_angas.nakshatras_with_ends[-2]
      (nakshatra_ID, nakshatra_end_jd) = (nakshatra_span.anga.index, nakshatra_span.jd_end)
      nakshatra_dev = names.NAMES['NAKSHATRA_NAMES']['sa'][scripts[0]][nakshatra_ID]
      nakshatra_eng = names.translate_or_transliterate(text=nakshatra_dev,source_script=sanscript.DEVANAGARI, script=sanscript.HK)
      nakshatra = names.translate_or_transliterate(text=nakshatra_dev, source_script=sanscript.DEVANAGARI, script=sanscript.TAMIL)
      if nakshatra_span.jd_end is not None and  nakshatra_span.jd_end > previous_day_panchaanga.day_length_based_periods.fifteen_fold_division.saura.jd_start:
        nakshatra_data_str = 'prev{anga{%s-%s-%s}{time{*%s}{%s}}}hspace{1ex}' % \
                        (nakshatra_eng,nakshatra_dev,nakshatra,
                         # time.Hour(24 * (nakshatra_end_jd - previous_day_panchaanga.jd_sunrise)).to_string(format='gg-pp'),
                         _get_relative_nadikas(nakshatra_end_jd, daily_panchaanga),
                         time.Hour(24 * (nakshatra_end_jd - jd)).to_string(format=time_format)) + nakshatra_data_str

  return nakshatra_data_str

panchaanga = annual.get_panchaanga_for_civil_year(city=city, year=yyyy,allow_precomputed=False)

daily_panchaangas = panchaanga.daily_panchaangas_sorted()

for d, daily_panchaanga in enumerate(daily_panchaangas):
    [year, month, dat] = [daily_panchaanga.date.year, daily_panchaanga.date.month, daily_panchaanga.date.day]
    if month==mon and dat==dd:
        print(f'Drilling down to {year},{month},{dat}')
        if d == 0:
            previous_day_panchaanga = None
        else:
            previous_day_panchaanga = daily_panchaangas[d - 1]
        if daily_panchaanga.date < panchaanga.start_date or daily_panchaanga.date > panchaanga.end_date:
            continue
        [y, m, dt] = [daily_panchaanga.date.year, daily_panchaanga.date.month, daily_panchaanga.date.day]

        # checking @ 6am local - can we do any better?
        local_time = tz(panchaanga.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
        # compute offset from UTC in hours
        tz_off = (datetime.utcoffset(local_time).days * 86400 +
                    datetime.utcoffset(local_time).seconds) / 3600.0
        
        nakshatra_data_str = get_nakshatra_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga, include_early_end_angas=True)
        print(nakshatra_data_str)


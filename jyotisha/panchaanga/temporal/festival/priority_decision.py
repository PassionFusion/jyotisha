import logging

from jyotisha.panchaanga.temporal import zodiac


def decide_paraviddha(d0_angas, d1_angas, target_anga):
  # Doesn't seem to be equivalent to prior logic - hence not calling for now.
  prev_anga = target_anga - 1
  next_anga = target_anga + 1

  if (d0_angas.end == target_anga and d1_angas.end == target_anga) or (
      d1_angas.start == target_anga and d1_angas.end == target_anga):
    # Incident at kaala on two consecutive days; so take second
    fday = 1
  elif d0_angas.start == target_anga and d0_angas.end == target_anga:
    # Incident only on day 1, maybe just touching day 2
    fday = 0
  elif d0_angas.end == target_anga:
    fday = 0
  elif d1_angas.start == target_anga:
    fday = 0
  elif d0_angas.start == target_anga and d0_angas.end == next_anga:
    if d0_angas.interval.name == 'aparaahna':
      fday = 0
    else:
      fday = 0 - 1
  elif d0_angas.end == prev_anga and d1_angas.start == next_anga:
    fday = 0
  else:
    fday = None
  return fday


def decide_puurvaviddha(d0_angas, d1_angas, target_anga):
  # Doesn't seem to be equivalent to prior logic - hence not calling for now.
  kaala = d0_angas.interval.name
  prev_anga = target_anga - 1
  next_anga = target_anga + 1
  if d0_angas.start >= target_anga or d0_angas.end >= target_anga:
    fday = 0
  elif d1_angas.start == target_anga or d1_angas.end == target_anga:
    fday = 0 + 1
  else:
    # This means that the correct anga did not
    # touch the kaala on either day!
    if d0_angas.end == prev_anga and d1_angas.start == next_anga:
      # d_offset = {'sunrise': 0, 'aparaahna': 1, 'moonrise': 0, 'madhyaahna': 1, 'sunset': 1}[kaala]
      d_offset = 0 if kaala in ['sunrise', 'moonrise'] else 1
      # Need to assign a day to the festival here
      # since the anga did not touch kaala on either day
      # BUT ONLY IF YESTERDAY WASN'T ALREADY ASSIGNED,
      # THIS BEING PURVAVIDDHA
      # Perhaps just need better checking of
      # conditions instead of this fix
      fday = 0 + d_offset
    else:
      logging.info("%s, %s, %s - Not assigning a festival this day. Likely the next then.", str(d0_angas.to_tuple()), str(d1_angas.to_tuple()), str(target_anga.index))
      fday = None
  return fday


def decide_aparaahna_vyaapti(d0_angas, d1_angas, target_anga, ayanaamsha_id):
  # Doesn't seem to be equivalent to prior logic - hence not calling for now.
  if d0_angas.interval.name != 'aparaahna':
    return None

  prev_anga = target_anga - 1
  next_anga = target_anga + 1
  p, q, r = prev_anga, target_anga, next_anga  # short-hand
  # Combinations
  # (p:0, q:1, r:2)
  # <j> ? r ? ?: d
  # <a> ? ? q q: d + 1
  # <b> ? p ? ?: d + 1
  # <e> p q q r: vyApti
  # <h> q q ? r: d
  # <i> ? q r ?: d
  if d0_angas.end > q:
    # One of the cases covered here: Anga might have been between end of previous day's interval and beginning of this day's interval. Then we would have: r r for d1_angas.
    fday = 0
  elif d1_angas.start == q and d1_angas.end == q:
    fday = 1
  elif d0_angas.end < q and d1_angas.start >= q:
    # Covers p p r r, [p, p, q, r], [p, p, q, q]
    fday = 1
  elif d0_angas.start == q and d0_angas.end == q and d1_angas.end > q:
    fday = 0
  elif d0_angas.end == q and d1_angas.start > q:
    fday = 0
  elif d0_angas.end == q and d1_angas.start == q:
    anga_span = zodiac.AngaSpanFinder(ayanaamsha_id=ayanaamsha_id, anga_type=target_anga.get_type()).find(jd1=d0_angas.interval.jd_start, jd2=d1_angas.interval.jd_end, target_anga_in=target_anga)
    vyapti_1 = max(d0_angas.interval.jd_end - anga_span.jd_start, 0)
    vyapti_2 = max(anga_span.jd_end - d1_angas.interval.jd_start, 0)
    if vyapti_2 > vyapti_1:
      fday = 0 + 1
    else:
      fday = 0
  else:
    logging.info("%s, %s, %s.", str(d0_angas.to_tuple()), str(d1_angas.to_tuple()), str(target_anga.index))
    fday = None
  return fday


'''
Scripts to practice some of the "Secrets
of Mental Math" a book with techniques
written by Arthur T. Benjamin
'''
from numpy.random import choice, randint
import numpy as np
import time
from random import randrange
from datetime import datetime
from datetime import timedelta
import json

if False:
  import androidhelper
  droid = androidhelper.Android()
else:
  droid = None

def say(text):
  if droid is not None:
    droid.ttsSpeak(text)
  else:
    print(text)

class ProblemInterface:

  def __init__(self, pause, **kwargs):
    self.pause = pause

  #* init, pause, any selection, which holidays, date range
  def human_readable(self) -> (str, str):
    raise NotImplementedError("Inheriting class needs to implement this")

  def generate_quiz(num_problems, **kwargs):# -> Quiz:
    raise NotImplementedError("Inheriting class needs to implement this")

  def match_answer(self, answer) -> bool:
    raise NotImplementedError("Inheriting class needs to implement this")

  def to_latex(self) -> (str, str):
    raise NotImplementedError("Inheriting class needs to implement this")

  def ask_pause_answer(self) -> None:
    """Ask aloud, pause, answer"""
    problem, answer = self.human_readable()
    droid.ttsSpeak(problem)
    time.sleep(self.pause)
    droid.ttsSpeak(answer)

  def print_pause_answer(self) -> None:
    """Print aloud, pause, answer"""
    problem, answer = self.human_readable()
    print(problem)
    time.sleep(self.pause)
    print(answer)

  def ask_input(self) -> bool:
    """ask input"""
    problem, answer = self.human_readable()
    droid.ttsSpeak(problem)
    your_answer = input()
    return self.match_answer(your_answer)

  def print_input(self) -> bool:
    """print input"""
    problem, answer = self.human_readable()
    print(problem)
    your_answer = input()
    return self.match_answer(your_answer)


class Quiz:

  def __init__(self, problems, log=None):#: list(ProblemInterface)
    self.problems = problems
    self.finished = False
    self.log = log

  def worksheet(self, speak=True, grade=True, write=True):
    grades = []
    times = []
    for problem in self.problems:
      q, a = problem.human_readable()
      if speak:
        say(q)
      if write:
        print(q)
      if grade:
        t1 = time.time()
        answer = input()
        t2 = time.time()
        grades.append(problem.match_answer(answer))
        times.append(t2 - t1)
      else:
        time.sleep(problem.pause)
      if speak:
        say(a)
      if write:
        print(a)
    self.grades = grades
    self.times = times
    self.finished = True
    if self.log is not None:
      with open(self.log, 'a+') as f:
        f.write(self.get_summary())
    print(self.get_summary())


  def get_summary(self):
    if not self.finished:
      raise RuntimeError("Complete the worksheet before getting a summary")
    summary = {
                "problem_count": len(self.problems),
                "correct_count": int(np.sum(self.grades)),
                "total_time": float(np.sum(self.times)),
                "mean_time": float(np.mean(self.times)),
                "max_time": float(np.max(self.times)),
                "median_time": float(np.median(self.times)),
                "std_time": float(np.std(self.times)),
                "correct": float(np.mean(self.grades)),
              }
    return json.dumps(summary)

class DayOfTheWeek(ProblemInterface):

  def datetime_to_calendar(dt: datetime):
    '''Convert month day year'''
    months = ['January', 'February',
              'March', 'April', 'May',
              'June', 'July', 'August',
              'September', 'October',
              'November', 'December']
    month = months[dt.month-1]
    return f'{month} {dt.day} {dt.year}'

  def weekday_to_name(day: int) -> str:
    days = {
      0: 'sunday',
      1: 'monday',
      2: 'tuesday',
      3: 'wednesday',
      4: 'thursday',
      5: 'friday',
      6: 'saturday',
      }
    return days[day]

  def name_to_weekday(day: str) -> int:
    days = {
      'sunday': 0,
      'monday': 1,
      'tuesday': 2,
      'wednesday': 3,
      'thursday': 4,
      'friday': 5,
      'saturday': 6,
      }
    return days[day.lower()]

  def random_date(start, end):
    """
    This function will return a random
    datetime between two datetime objects.
    """
    delta = end - start
    day_secs = delta.days * 24 * 60 * 60
    int_delta = day_secs + delta.seconds
    random_second = randrange(int_delta)
    td = timedelta(seconds=random_second)
    return start + td

  def generate_quiz(num_problems,
                    start=datetime(1780, 1, 1),
                    end=datetime(2050, 1, 1),
                    pause=20):# -> Quiz:
    problems = []
    for k in range(num_problems):
      dt = random_date(start, end)
      problems.append(DayOfTheWeek(dt, pause=pause))
    return Quiz(problems)

  def __init__(self, date_time, pause=20):
    super(DayOfTheWeek, self).__init__(pause)
    self.date_time = date_time
    self.answer = (self.date_time.weekday() + 1) % 7

  def human_readable(self) -> (str, str):
    caldt = DayOfTheWeek.datetime_to_calendar(self.date_time)
    q = f'What day of the week was {caldt}?'
    a = f'{caldt} was a {DayOfTheWeek.weekday_to_name(self.answer)}'
    return q, a

  def match_answer(self, answer) -> bool:
    "supports 3, Wednesday, wednesday"
    try:
      answer = int(answer)
    except:
      answer = DayOfTheWeek.name_to_weekday(answer)
    return self.answer == answer

  def to_latex(self) -> (str, str):
    #TODO
    pass


class FloatingHoliday(ProblemInterface):

  holidays = {
    'Thanksgiving Day': {
     'weekday': 4, 'week': 4, 'month': 11},
    'Martin Luther King Junior Day': {
     'weekday': 1, 'week': 3, 'month': 1},
    'Presidents Day': {
     'weekday': 1, 'week': 3, 'month': 2},
    'Memorial Day': {
     'weekday': 1, 'week': 5, 'month': 5},
    'Labor Day': {
     'weekday': 1, 'week': 1, 'month': 9},
    'Columbus Day': {
     'weekday': 1, 'week': 2, 'month': 10},
    }

  def floating_holiday(holiday, year):
    """
    Given a year and a holiday return the
    datetime object
    """
    if holiday['week'] == 5:
      return FloatingHoliday.floating_last_day(holiday, year)
    for k in range(1, 8):
      day = int((holiday['week']-1)*7 + k)
      dt = datetime(year, holiday['month'],
                    day)
      wkday = dt.weekday() + 1
      if wkday == holiday['weekday']:
        return dt
    raise Exception

  def floating_last_day(holiday, year):
    """
    Given a year and a holiday return the
    datetime object representing the last
    day of the month with the given weekday
    """
    month = (holiday['month'] + 1) % 12
    weekday = holiday['weekday']
    for k in range(1, 8):
      dt = datetime(year, month, 1)
      day_secs = k * 24 * 60 * 60
      td = timedelta(seconds=day_secs)
      holiday_dt = dt - td
      wkday = (holiday_dt.weekday() + 1) % 7
      if wkday == weekday:
        return holiday_dt
    raise Exception

  def generate_quiz(num_problems,
                    start=1780,
                    end=2050,
                    pause=20):# -> Quiz:
    problems = []
    years = range(start, end)
    holidays = list(FloatingHoliday.holidays.keys())
    rng = range(len(holidays))
    hs = choice(rng, (num_problems, ))
    for h in hs:
      holiday = holidays[h]
      year = choice(years, (1,))[0]
      problems.append(FloatingHoliday(holiday, year, pause))
    return Quiz(problems)

  def __init__(self, holiday, year, pause=30):
      super(FloatingHoliday, self).__init__(pause)
      self.holiday = holiday
      self.year = year
      holiday = FloatingHoliday.holidays[self.holiday]
      self.dt = FloatingHoliday.floating_holiday(holiday, year)
      self.calendar_date = date_time2calendar(self.dt)

  def human_readable(self) -> (str, str):
    h = f'{self.holiday} of {self.year}'
    q = f'What day of the month was {h}'
    a = f'{h} was {self.calendar_date}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
        answer = int(answer)
    except:
        pass
    return self.dt.day == answer

  def to_latex(self) -> (str, str):
    #TODO
    pass


class Addition(ProblemInterface):

  def generate_quiz(num_problems, digits_1=1, digits_2=1, pause=30):# -> Quiz:
    range1 = range(10**(digits_1-1), 10**digits_1)
    range2 = range(10**(digits_2-1), 10**digits_2)
    x = choice(range1, (num_problems, ),
               False if num_problems<(10**digits_1) else True)
    y = choice(range2, (num_problems, ),
               False if num_problems<(10**digits_2) else True)
    problems = []
    for a, b in zip(x, y):
      problems.append(Addition(a, b, pause))
    return Quiz(problems)

  def __init__(self, operand_1, operand_2, pause=30):
      super(Addition, self).__init__(pause)
      self.operand_1 = operand_1
      self.operand_2 = operand_2
      self.answer = operand_1 + operand_2

  def human_readable(self) -> (str, str):
    problem = f'{self.operand_1} plus {self.operand_2}'
    q = f'What is {problem}'
    a = f'{problem} equals {self.answer}'
    return q, a

  def match_answer(self, answer) -> bool:
    try:
      answer = int(answer)
    except:
      pass
    return answer == self.answer

  def to_latex(self) -> (str, str):
    #TODO
    pass



if __name__ == '__main__':
  #dotw = DayOfTheWeek(dt, pause=5)
  #dotw.print_pause_answer()
  #print(dotw.print_input())
  #fh = FloatingHoliday("Thanksgiving Day", 2021, pause=5)
  #fh.print_pause_answer()
  #print(fh.print_input())
  #additions = Addition(6, 7, pause=5)
  #additions.print_pause_answer()
  #print(additions.print_input())
  #ps = Addition.generate_quiz(10, digits_1=1, digits_2=1, pause=30)
  #ps.worksheet(speak=False)
  ps = DayOfTheWeek.generate_quiz(10)
  ps.worksheet(speak=False)
  ps = FloatingHoliday.generate_quiz(10)
  ps.worksheet(speak=False)


# vim: set ts=2 sts=2 et sw=2 ft=python:

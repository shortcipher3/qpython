import androidhelper
import numpy as np
import time
from random import randrange
from datetime import datetime
from datetime import timedelta
#from __future__ import division

droid = androidhelper.Android()

def say(text):
    droid.ttsSpeak(text)

def date_time2calendar(dt):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return months[dt.month-1] + ' ' + str(dt.day) + ', ' + str(dt.year)

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def weekday(dt):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[dt.weekday()]


def multiplication(num_problems=10, pause=30, digits_1=2, digits_2=2):
    say('multiplication of ' + str(digits_1) + ' digit numbers by ' + str(digits_2) + ' digit numbers')
    x = np.random.choice(range(10**(digits_1-1), 10**digits_1), (num_problems, ), False)
    y = np.random.choice(range(10**(digits_2-1), 10**digits_2), (num_problems, ), True)
    for k in range(num_problems):
        say('What is ' + str(x[k]) + ' times ' +  str(y[k]))
        time.sleep(pause)
        say(str(x[k]) + ' times ' +  str(y[k]) + ' equals ' + str(x[k]*y[k]))

def addition(num_problems=10, pause=30, digits_1=2, digits_2=2):
    say('addition of ' + str(digits_1) + ' digit numbers by ' + str(digits_2) + ' digit numbers')
    x = np.random.choice(range(10**(digits_1-1), 10**digits_1), (num_problems, ), False)
    y = np.random.choice(range(10**(digits_2-1), 10**digits_2), (num_problems, ), False)
    for k in range(num_problems):
        say('What is ' + str(x[k]) + ' plus ' +  str(y[k]))
        time.sleep(pause)
        say(str(x[k]) + ' plus ' +  str(y[k]) + ' equals ' + str(x[k]+y[k]))

def subtraction(num_problems=10, pause=30, digits_1=2, digits_2=2):
    say('subtraction of ' + str(digits_1) + ' digit numbers by ' + str(digits_2) + ' digit numbers')
    x = np.random.choice(range(10**(digits_1-1), 10**digits_1), (num_problems, ), False)
    y = np.random.choice(range(10**(digits_2-1), 10**digits_2), (num_problems, ), False)
    for k in range(num_problems):
        say('What is ' + str(x[k]) + ' minus ' +  str(y[k]))
        time.sleep(pause)
        say(str(x[k]) + ' minus ' +  str(y[k]) + ' equals ' + str(x[k]-y[k]))

def whole_roots(num_problems=10, pause=30, digits=2, n=2):
    say('whole ' + str(n) + ' roots of ' + str(digits) + ' digit numbers ')
    x = np.random.choice(range(10**(digits-1), 10**digits), (num_problems, ), False)
    for k in range(num_problems):
        say('What is the ' + str(n) + ' root of ' + str(x[k]**n) + '?')
        time.sleep(pause)
        say('The ' + str(n) + ' root of ' + str(x[k]**n) + ' is ' + str(x[k]))

def roots(num_problems=10, pause=30, digits=2, n=2):
    say(str(n) + ' roots of ' + str(digits) + ' digit numbers ')
    x = np.random.choice(range(10**(digits-1), 10**digits), (num_problems, ), False)
    for k in range(num_problems):
        say('What is the ' + str(n) + ' root of ' + str(x[k]) + '?')
        time.sleep(pause)
        say('The ' + str(n) + ' root of ' + str(x[k]) + ' is ' + str(x[k]**(1.0/n)))

def powers(num_problems=10, pause=30, digits=2, n=2):
    say(str(n) + ' powers of ' + str(digits) + ' digit numbers ')
    x = np.random.choice(range(10**(digits-1), 10**digits), (num_problems, ), False)
    for k in range(num_problems):
        say('What is ' + str(x[k]) + ' to the power of ' + str(n) + '?')
        time.sleep(pause)
        say(str(x[k]) + ' to the power of ' + str(n) + ' equals ' + str(x[k]**(n)))

def calendar_days(num_problems=10, pause=30):
    say('days of the week')
    dates = [random_date(datetime(1780, 1, 1), datetime(2020, 1, 1)) for k in range(num_problems)]
    for date in dates:
        say('What day of the week was ' + date_time2calendar(date) + '?')
        time.sleep(pause)
        say(date_time2calendar(date) + ' was a ' + weekday(date))

def modulo(num_problems=10, pause=30, digits=6, modulo=9):
    say('modulo ' + str(modulo))
    for k in range(num_problems):
        n = np.random.randint(10**(digits-1), 10**digits)
        say('What is ' + str(n) + ' modulo ' + str(modulo))
        time.sleep(pause)
        say(str(n) + ' modulo ' + str(modulo) + ' is ' + str(n % modulo))

def pegs(num_problems=10,
	        n_digits=2,
	        pause=5):
    #TODO give sounds/words not ready
    say('major system pegs')
    smallest = 10**(n_digits-1)
    largest = 10**(n_digits)-1
    randint = np.random.randint
    ns = randint(smallest,
    	             largest,
    	             (num_problems,))
    for n in ns:
        say(f'Peg {n}')
        time.sleep(pause)
        say(f'Pegged {n}')

def peg(num_problems=10, pause=5):
    # not ready
    say('major system pegs')
    for k in range(num_problems):
        operands = np.random.randint(0, 10, (10, 2))
        for x, y in operands:
            say('Peg ' + str(x*10+y))
            time.sleep(pause)
        say('The complete number is:')
        time.sleep(pause)
        say(' '.join([str(x) + ' ' + str(y) for x, y in operands]))

def memorize(num_problems=10, pause=5):
    # not ready
    say('major system pegs')
    for k in range(num_problems):
        operands = np.random.randint(0, 10, (10, 2))
        for x, y in operands:
            say('Peg ' + str(x*10+y))
            time.sleep(pause)
        say('The complete number is:')
        time.sleep(pause)
        say(' '.join([str(x) + ' ' + str(y) for x, y in operands]))

#TODO Thanksgiving 2021 to calendar date
# Thanksgiving 4th Thursday
# Martin Luther King Jr Day 3rd Monday in January
# Presidents Day 3rd Monday in February
# Memorial day last Monday in May
# Labor day first Monday in September
# Columbus day 2nd Monday in October

pegs(1)
#modulo(num_problems=2, pause=30, digits=6, modulo=9)
#whole_roots(num_problems=2, pause=10, digits=2, n=3)
#whole_roots(num_problems=2, pause=10, digits=2, n=2)
#roots(num_problems=2, pause=10, digits=2, n=2)
#roots(num_problems=2, pause=10, digits=2, n=3)
#powers(num_problems=2, pause=30, digits_1=2, digits_2=2)
#powers(num_problems=2, pause=30, digits_1=2, digits_2=3)
#calendar_days(num_problems=2, pause=30)
#memorize(num_problems=2, pause=5)
#multiplication(num_problems=2, pause=10, digits_1=2, digits_2=1)
#subtraction(num_problems=2, pause=10, digits_1=2, digits_2=1)
#addition(num_problems=2, pause=10, digits_1=2, digits_2=1)



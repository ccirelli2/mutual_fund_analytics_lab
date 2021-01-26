"""
Purpose : Determine which text matching approach is more efficient.
"""

# Import Python Modules
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime

# Import Project Modules
from functions_decorators import *

# Declare Variables
text = 'today is a good day to code!'
token = 'code'
iterations = 100000


@my_timeit
def str_init(text, token, iterations):

    for i in range(iterations):
        if token in text:
            pass
        else:
            pass
    
@my_timeit
def str_find(text, token, iterations):

    for i in range(iterations):
        if text.find(token) != -1:
            pass
        else:
            pass




str_init(text, token, iterations)
str_find(text, token, iterations)


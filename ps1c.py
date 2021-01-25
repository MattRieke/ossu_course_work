# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 06:43:03 2021

@author: mattr
"""

import sys

#request inputs from user
annual_salary = float(input('Enter the starting salary: '))

#initialize values
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25 * total_cost
r = 0.04

#guess and check setup
epsilon = 100.00
number_guess = 0
current_savings = 0
low = 0
high = 10000

while abs(current_savings - portion_down_payment) >= epsilon:
    #reinitialize values
    current_savings = 0
    monthly_salary = annual_salary/12
    guess_val = int((low + high)/2)
    month=0
    while month < 36:
        #evaluate savings over 36 months
        current_savings += current_savings*r/12 + monthly_salary * guess_val/10000
        month += 1
        if month % 6 == 0:
            monthly_salary *= (1+semi_annual_raise)
    if current_savings < portion_down_payment:
        #eliminate bottom bisection
        low = guess_val
    else:
        #eliminate high bisection
        high = guess_val
    number_guess += 1
    if guess_val ==9999:
        #Try searching 100% rate if 99.99 is not enough
        low = 10000
    if guess_val > 9999 and abs(current_savings - portion_down_payment) >= epsilon:
        #Savings condition not possible with salary
        print('It is not possible to pay the down payment in three years.')
        sys.exit()

#print(current_savings)
print('Best savings rate:', str(guess_val/10000))
print('Steps in bisection search:', str(number_guess))
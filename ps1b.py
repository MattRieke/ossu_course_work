# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 06:12:32 2021

@author: mattr
"""

#request inputs from user
annual_salary = float(input('Enter your starting annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal: '))

#initialize values
portion_down_payment = 0.25 * total_cost
current_savings = 0
monthly_salary = annual_salary/12
r = 0.04
months = 0

#track months, add interest, add monthly savings
while current_savings < portion_down_payment:
    months += 1
    current_savings += current_savings*r/12
    current_savings += monthly_salary * portion_saved
    if months % 6 == 0:
        monthly_salary *= (1+semi_annual_raise)

print('Number of months:', months)
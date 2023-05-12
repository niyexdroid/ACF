'''
This is a utilities file containing special functions to carry out some 
form of processing.
'''

from django.core.paginator import Paginator, EmptyPage
import math

def PaginateObjects(queryset:list, page_number, page_size:int):
    paginator = Paginator(queryset, page_size)
    
    # this targets the input of the page number and tackles some edge cases
    try:
        page_number = int(float(page_number))
        objects = paginator.page(int(float(page_number)))
    except EmptyPage:
        if page_number > paginator.num_pages:
            objects = paginator.page(paginator.num_pages); page_number = paginator.num_pages
        else:
            objects = paginator.page(1); page_number = 1
    except ValueError:
        objects = Paginator.page(1); page_number = 1
        
    
    number_of_paginate_buttons = 5
    
    '''
    diff_left is basically the difference between the current page number and the first pagination button.
    By default, the diff_left will match up so that the current page number will be in the middle of the pagination buttons.
    The left index, which will be included as one of the pagination buttons , is gotten by subtracting diff_left from the current page number.
    Note that this is the default behaviour of the Paginator, assuming there are enough pagination buttons to the left of the current page number.
    '''

    diff_left = math.ceil((number_of_paginate_buttons/2) - 1)
    left_index = page_number - diff_left
    

    '''
    if there are not enough pagination buttons to the left of the current page number,
    then we immediately calculate the right index from the standpoint of the left index,
    then we return our custom range, and this function is done.
    '''

    if left_index < 1:
        left_index = 1
        right_index = number_of_paginate_buttons
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages
        custom_range = range(left_index, right_index + 1)
        return custom_range, objects, paginator

    '''
    diff_right is basically the difference between the current page number and the last pagination button.
    By default, the diff_right will match up so that the current page number will be in the middle of the pagination buttons.
    The right index, which will be included as one of the pagination buttons , is gotten by adding diff_right to the current page number.
    Note that this is the default behaviour of the Paginator, assuming there are enough pagination buttons to the right of the current page number.
    '''

    
    diff_right = math.floor(number_of_paginate_buttons/2)
    right_index = page_number + diff_right 
    
    '''
    if there are not enough pagination buttons to the right of the current page number,
    then we immediately calculate the left index from the standpoint of the right index,
    then we return our custom range, and this function is done.
    '''

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages
        left_index = paginator.num_pages - number_of_paginate_buttons + 1
        if left_index < 1:
            left_index = 1
    
    '''
    provided that there are enough pagination buttons to the left of the current page number and to the right of the current page number,
    i.e the page_number is probably somewhere between the total number of pagination buttons,
    then we calculate the custom range with the calculated left and right indices.
    '''
    
    custom_range = range(left_index, right_index+1)
    return custom_range, objects, paginator
    
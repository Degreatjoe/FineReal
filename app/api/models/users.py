#!/usr/bin/python3

#from api import app, db
from  app.models.user import User

def to_dict_users(is_teacher=False, include_email=False):
    '''
    This function help to structure user data for easy serialization
    '''
    data = {
        'id': User.id,
        'first_name': User.first_name,
        'middle_name': User.middle_name,
        'last_name': User.last_name,
        'date_of_birth': User.dob,
        'status': User.is_verified,
        'role': User.role,
        'enrolled_cources': [cource for cource in User.enrolled_courses],
        'number of_enrolled_cources': count_cources(),
        
        'linke': {
            'self': 'link_to_self'
        }
    }
    if include_email:
        data['email'] = User.email
    
    if is_teacher:
        pass
        
    return data



def count_cources():
    pass
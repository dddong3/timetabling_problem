'''
chromosome =
[
    {
        'course_id': '12345',
        'course_name': '計算機概論',
        'class_id': '36101',
        'teacher_list': [
            'teacher_1',
            'teacher_2'
        ],
        'week': 1,
        'session': '20',
        'classroom': 'A101'
    }
]        
'''



'''
teacher_class_week = 
{
    'teacher_1': {
        1: {
            '01': 2,
            '02': 1,
            '03': 0,
            ...
        }
        2: {
            '01': 2,
            '02': 1,
            '03': 0,
            ...
        },
        ...
    },
}

if 規則太多改成加分fun和減分fun維護
'''

'''
course_week =
{
    '12345': {
        '1': {
            '01': 2,
            '02': 1,
            '03': 0,
            ...
        }
    }
}
'''
import json


def wash_gene() -> None:
    FILE_NAME = 'test_gene.json'

    course_obj = json.load(open(FILE_NAME, 'r', encoding='utf-8'))

    teacher_list = set()

    for course in course_obj:
        for teacher in course['teacher_list']:
            teacher_list.add(teacher['teacher_name'])
        if len(course['teacher_list']) == 0: #週會沒老師
            null_teacher_id = '梅姥釃'
            # null_teacher_id = 'NULL'
            course['teacher_list'].append({'teacher_name': null_teacher_id})
            teacher_list.add(null_teacher_id)

    gene = []

    for course in course_obj:
        current_course_template = {
            'course_id': course['course_id'],
            'course_name': course['course_name'],
            'course_type': course['course_type'],
            'class_id': course['class_id'],
            'session_length': None,
            'teacher_list': None,
            'week': None,
            'session': None,
            'classroom': None
        }

        current_course_template['course_key'] = current_course_template['course_id'] + current_course_template['class_id']

        sector_dict = {}
        for time, teacher in zip(course['time_list'], course['teacher_list']):
            # print(time, teacher)
            session_count = 0
            for sector in time['sector']:
                session_count += 1
            if sector_dict.get(sector) == None:
                sector_dict[sector] = current_course_template.copy()
                sector_dict[sector]['teacher_list'] = []
                sector_dict[sector]['week'] = time['weekday']
                sector_dict[sector]['session'] = sector
                sector_dict[sector]['session_length'] = session_count
                sector_dict[sector]['classroom'] = course.get('classroom', [None])[0]

            sector_dict[sector]['teacher_list'].append(teacher['teacher_name'])

        gene.extend(list(sector_dict.values()))

    json.dump(gene, open('test_gene_washed.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

def wash_class() -> None:
    class_dict = {}
    FILE_NAME = 'test_gene.json'
    course_obj = json.load(open(FILE_NAME, 'r', encoding='utf-8'))
    for course in course_obj:
        for classroom in course['classroom']:
            if len(classroom) == 0:
                continue
            class_dict[classroom] = {
                "size":None,
                "type": None,
                "building": None
            }

            if classroom[0].isascii():
                class_dict[classroom]['building'] = classroom[0]
    
    json.dump(class_dict, open('class.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

if __name__ == '__main__':
    wash_gene()
    # wash_class()
import camelot
import PyPDF2
import re
import json


def get_approved_courses(path=''):
    table_number = 0
    tables = camelot.read_pdf(path, pages='all')
    actual_table_df = None
    # Parte 1: Obter lista de materias ja cursadas que o estudante ja passou.

    materia_atual = None
    materias_aprovado = []

    actual_table_df = tables[table_number].df
    while len(actual_table_df.columns) == 9:
        for index, elem in actual_table_df.iterrows():
            materia_atual = {
                'title': elem[3],
                'note': elem[7],
                'id': elem[2],
                'credits': elem[4],
                'approved': False
            }
            if materia_atual['note'] in ["MM", "MS", "SS"]:
                materia_atual['approved'] = True
                materias_aprovado.append(materia_atual)
        table_number += 1
        actual_table_df = tables[table_number].df
    return materias_aprovado


def get_missing_courses(program_id, approved_courses, selected_optional_courses_ids):
    courses = json.load(open("courses.json", "r"))
    optional_courses = json.load(open("optional_courses.json", "r"))
    all_courses = [*courses[program_id], *optional_courses[program_id]]
    approved_courses_temp = approved_courses

    for approved_course in approved_courses:

        approved_course_index = None

        for (index, course) in enumerate(courses[program_id]):
            if course["id"] == approved_course["id"]:
                approved_course_index = index
                break

        if approved_course_index != None:
            courses[program_id].pop(approved_course_index)

    if selected_optional_courses_ids is not None:
        print("entrou?")

        for selected_optional_courses_id in selected_optional_courses_ids:
            course_and_prerequisites = [selected_optional_courses_id]

            for course_id in course_and_prerequisites:
                found_course = next(
                    (c for c in all_courses if course_id == c["id"]), None)

                if found_course and len(found_course["prerequisites"]) > 0:
                    for prerequisite_id in found_course["prerequisites"]:
                        course_and_prerequisites.append(prerequisite_id)

            print(course_and_prerequisites)

            missing_courses = []
            for prerequisite_id in course_and_prerequisites:

                already_added = next(
                    (c for c in courses[program_id] if prerequisite_id == c["id"]), None)

                already_approved = next(
                    (c for c in approved_courses_temp if prerequisite_id == c["id"]), None)

                if not already_approved and not already_added:
                    missing_course = next(
                        (c for c in all_courses if prerequisite_id == c["id"]), None)

                    if missing_course:
                        courses[program_id].append(missing_course)

    return courses[program_id]


def get_program_id(path=''):
    curriculo = ""
    with open(path, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        page = reader.getPage(0)
        text = page.extractText()
        regex_curriculo = re.search(r"(\d{4}/-?\d)", text)
        curriculo = regex_curriculo.group(1)
    return(curriculo)

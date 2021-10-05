import camelot
import PyPDF2
import re

def extrair_materias_aprovado(path=''):
    table_number = 0
    tables = camelot.read_pdf(path,pages='all')
    actual_table_df = None
    #Parte 1: Obter lista de materias ja cursadas que o estudante ja passou.

    materia_atual = None
    materias_aprovado = []

    actual_table_df = tables[table_number].df
    while len(actual_table_df.columns) == 9:
        for index,elem in actual_table_df.iterrows():
            materia_atual = {
                'title': elem[3],
                'note': elem[7],
                'id': elem[2],
                'workload': elem[4],
                'approved': False
            }
            if materia_atual['note'] in ["MM" ,"MS","SS"]:
                materia_atual['approved'] = True
                materias_aprovado.append(materia_atual)
        table_number += 1
        actual_table_df = tables[table_number].df
    return materias_aprovado

def extrair_numero_curriculo(path=''):
    curriculo = ""
    with open(path, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        page = reader.getPage(0)
        text = page.extractText()
        regex_curriculo = re.search(r"(\d{4}/-?\d)",text)
        curriculo = regex_curriculo.group(1)
    return(curriculo)

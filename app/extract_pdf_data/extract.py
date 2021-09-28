import camelot
from  materia import Materia

path = '../uploads/historico.pdf'

table_number = 0
tables = camelot.read_pdf(path,pages='all')
actual_table_df = None
#Parte 1: Obter lista de materias ja cursadas que o estudante ja passou.

materia_atual = None
materias_aprovado = []

actual_table_df = tables[table_number].df
while len(actual_table_df.columns) == 9:
    for index,elem in actual_table_df.iterrows():
        materia_atual = Materia(
            nome=elem[3],
            nota=elem[7],
            codigo=elem[2],
            carga_horaria=elem[4]
        )
        if materia_atual.aprovado:
            materias_aprovado.append(materia_atual)

    table_number += 1
    actual_table_df = tables[table_number].df

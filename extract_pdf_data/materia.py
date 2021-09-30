class Materia:
    def __init__(self,nome="",nota="-",codigo="",carga_horaria=0):
        self.nome = nome
        self.nota = nota
        self.codigo = codigo
        self.carga_horaria = carga_horaria

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self,var):
        self.__nota = var
        if var in ["MM" ,"MS","SS"]:
            self.aprovado = True
        else:
            self.aprovado = False

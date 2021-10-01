class Discipline:
    code = ""
    name = ""
    credit = ""
    prerequisite = []
    semester = ""
    note = ""
    workload = ""
    approved = ""

    def __init__(self,name="",note="-",code="",workload=0):
        self.name = name
        self.note = note
        self.code = code
        self.workload = workload

    @property
    def note(self):
        return self.__note

    @note.setter
    def note(self,var):
        self.__none = var
        if var in ["MM" ,"MS","SS"]:
            self.approved = True
        else:
            self.approved = False

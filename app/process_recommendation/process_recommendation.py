from itertools import product
from mip import Model, xsum, BINARY
import json


def getCourses():
  file = open('./courses.json')
  courses = json.load(file)
  file.close()
  return courses

def processRecommendation(idCurriculum, approvedCourses):
  courses = getCourses()

  notApprovedCourses = [{'id':'calouro', 'title': '', 'credits': '', 'prerequisites': []}]

  formado = {'id':'formado', 'title': '', 'credits': '', 'prerequisites': []}

  for course in courses['6360/1']:
    if not findFromArrayJson(course['id'], 'id', []):
      notApprovedCourses.append(course)
      formado['prerequisites'].append(course['id'])

  notApprovedCourses.append(formado)

  S = []

  for index, course in enumerate(notApprovedCourses): # mudar para id curriculum
    if index != 0: 
      if len(course['prerequisites']) != 0:
        for prerequisite in course['prerequisites']:
          dupla = None
          for z, notApprovedCourse in enumerate(notApprovedCourses):
            if (prerequisite == notApprovedCourse['id']):
              dupla = [z, index]
              break
          if (dupla != None):
            S.append(dupla)
          else: S.append([0, index])
      else: S.append([0, index])

  n = len(notApprovedCourses) - 2
  p = [0]
  u = [[0, 0]]
  c = [24, 0]

  for index in range(n):
    p.append(1)
    credit = notApprovedCourses[index + 1]['credits']
    u.append([credit, 0]) 
  p.append(0)
  u.append([0,0])

  (R, J, T) = (range(len(c)), range(len(p)), range(sum(p)))

  model = Model()

  x = [[model.add_var(name="x({},{})".format(j, t), var_type=BINARY) for t in T] for j in J]

  model.objective = xsum(t * x[n + 1][t] for t in T)

  for j in J:
      model += xsum(x[j][t] for t in T) == 1

  for (r, t) in product(R, T):
      model += (
          xsum(u[j][r] * x[j][t2] for j in J for t2 in range(max(0, t - p[j] + 1), t + 1))
          <= c[r])

  for (j, s) in S:
      model += xsum(t * x[s][t] - t * x[j][t] for t in T) >= p[j]

  model.optimize(max_seconds=3)
  response = []

  for (j, t) in product(J, T):
    if x[j][t].x >= 0.99:
      if (j != 0 and j < len(notApprovedCourses)):
        response.append({
          'id': notApprovedCourses[j]['id'],
          'title': notApprovedCourses[j]['title'],
          'period': t+p[j],
          'credits': notApprovedCourses[j]['credits'],
          'prerequisites': notApprovedCourses[j]['prerequisites']
        })
      print("Disciplina com id {}: começa em t={} e temina em t={}".format(j, t, t+p[j]))


  print("")
  print("Quantidade mínima de semestres para se formar = {}".format(model.objective_value))

  return response

def findFromArrayJson(value, fieldName, array):
  for i in array:
    if (value == i[fieldName]):
      return True
  return False
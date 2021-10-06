from itertools import product
from mip import Model, xsum, BINARY


def get_process_structure(courses, max_credits_by_period=20):
    coursesWithDummies = ["dummy", *courses, "dummy"]

    n = len(courses)

    p = list(map(lambda course:
                 0 if course == "dummy" else 1, coursesWithDummies))

    u = list(map(lambda course:
                 [0, 0] if course == "dummy" else [course["credits"], 0], coursesWithDummies))

    c = [max_credits_by_period, 0]

    S = []
    for courseIndex, course in enumerate(coursesWithDummies):
        if (course == "dummy"):
            continue

        if (len(course["prerequisites"]) == 0):
            S.append([0, courseIndex])
            continue

        for prerequisite in course["prerequisites"]:
            prerequisiteIndex = None

            for index, course in enumerate(courses):
                if course["id"] == prerequisite:
                    # print(course["id"], " é igual ", prerequisite)
                    prerequisiteIndex = index
                    break

            if prerequisiteIndex == None:
                continue

            S.append([prerequisiteIndex, courseIndex])
            coursesWithDummies[prerequisiteIndex]["isPrerequisite"] = True

    for courseIndex, course in enumerate(coursesWithDummies):
        if "isPrerequisite" in course:
            continue

        if courseIndex == len(coursesWithDummies) - 1:
            continue

        S.append([courseIndex, len(coursesWithDummies) - 1])

    return n, p, u, c, S


def process(n, p, u, c, S, courses):  # https://python-mip.readthedocs.io/en/latest/examples.html
    coursesWithDummies = ["dummy", *courses, "dummy"]

    recommendation = {
        "periods_to_graduate": 0,
        "periods": []
    }

    (R, J, T) = (range(len(c)), range(len(p)), range(sum(p)))

    model = Model()

    x = [[model.add_var(name="x({},{})".format(j, t), var_type=BINARY)
          for t in T] for j in J]

    model.objective = xsum(t * x[n + 1][t] for t in T)

    for j in J:
        model += xsum(x[j][t] for t in T) == 1

    for (r, t) in product(R, T):
        model += (
            xsum(u[j][r] * x[j][t2]
                 for j in J for t2 in range(max(0, t - p[j] + 1), t + 1))
            <= c[r])

    for (j, s) in S:
        model += xsum(t * x[s][t] - t * x[j][t] for t in T) >= p[j]

    model.optimize(max_seconds=3)

    recommendation["periods_to_graduate"] = int(model.objective_value)

    recommendation["periods"] = []
    for period in range(recommendation["periods_to_graduate"]):
        recommendation["periods"].append([])

    for (j, t) in product(J, T):
        if x[j][t].x >= 0.99:
            if j == 0 or j == len(coursesWithDummies) - 1:
                continue

            recommendation["periods"][t].append(coursesWithDummies[j])

    return recommendation

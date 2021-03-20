# My additional testing methods
def pointsMatch(models, points):
    if len(models) != len(points):
        return False

    for model in models:
        for point in points:
            if (pointMatch(model, point)):
                points.remove(point)
                break

    return len(points) == 0


def pointMatch(model, point):
    if model.scorer.username != point['scorer']:
        return False
    if model.typeOfPoint != point['typeOfPoint']:
        return False
    if model.scoredOn is not None:
        if model.scoredOn.username != point['scoredOn']:
            return False
    return True

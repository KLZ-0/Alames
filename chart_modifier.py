class Modifier:
    """
    Purpose: modifying chart series
    Chart overrides this class
    # NOTE: Use chart.series()[i].replace()
    """
    def __init__(self):
        pass

    def multiplyAll(self, ratio):
        self.ydata = []
        for serie in self.series():
            self.ydata.append([])
            vect = serie.pointsVector()
            for point in vect:
                point.setY(point.y()*ratio)
                self.ydata[-1].append(point.y())
            serie.replace(vect)
        self.updateAxes()

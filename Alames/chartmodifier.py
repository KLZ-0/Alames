from Alames.importer import *

from Alames import scope

class ChartModifier:
    """
    Purpose: modifying chart series
    Chart overrides this class
    # NOTE: Use chart.series()[i].replace() >> NEW: use chart.series()[i].setBaseData() to edit the whole series data
    # NOTE: ydata is not the same len as chart.series.. some series could be intentionally hidden and not present in ydata, therefore they are not displayed in the tracking tools
    """
    def __init__(self):
        self.filterAlamesOneApplied = False

    def filterAlamesOne(self):
        try:
            if self.filterAlamesOneApplied:
                scope.errorPopup("Filter already applied!")
                return
            self.series()[0].setName("Voltage")
            self.series()[1].setName("Current")
            self.series()[2].setName("State")

            voltageVect = self.selectionDataHolder.getYData(0)
            currentVect = self.selectionDataHolder.getYData(1)
            stateVect = self.selectionDataHolder.getYData(2)
            for i in range(len(stateVect)):
                state = stateVect[i]
                if state == 0:
                    pass
                elif state == 1:
                    voltageVect[i] = -voltageVect[i]
                elif state == 2:
                    currentVect[i] = -currentVect[i]
                elif state == 3:
                    voltageVect[i] = -voltageVect[i]
                    currentVect[i] = -currentVect[i]
                voltageVect[i] *= (3.62) # calibration
                currentVect[i] *= (1/2.54) # current calc

            self.selectionDataHolder.setYData(0, voltageVect)
            self.selectionDataHolder.setYData(1, currentVect)
            self.series()[2].hide()

            self.series()[0].setColor("#0000ff")
            self.series()[1].setColor("#ff0000")

            scope.window.updateChildren()

            self.filterAlamesOneApplied = True
        except:
            scope.errorPopup(traceback.format_exc())

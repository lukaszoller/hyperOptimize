import tkinter as tk
from src.hyperOptimizeApp.view.tools.RangeSlider import RangeSlider


class test_RangeSlider:

    def test_RangeSliderImpl(self):
        self.main = tk.Tk()
        # Konstanten
        WM_HEIGHT = 500
        WM_WIDTH = 800

        # Hauptfenster
        self.main.title("Test")
        self.main.geometry("{:}x{:}".format(WM_WIDTH, WM_HEIGHT))

        # Range slider
        sliderFrame = tk.Frame(self.main)
        sliderFrame.pack()
        self.rangeSlider = RangeSlider(sliderFrame,
                                       lowerBound=0, upperBound=200,
                                       initialLowerBound=25, initialUpperBound=75)
        self.rangeSlider.setMajorTickSpacing(50)
        self.rangeSlider.setMinorTickSpacing(10)
        self.rangeSlider.setPaintTicks(True)
        self.rangeSlider.setSnapToTicks(False)
        self.rangeSlider.setFocus()
        self.rangeSlider.pack()

        self.minValueEntry = tk.Entry(sliderFrame, textvariable=self.lowerBoundEntry)
        self.lowerEntryString.trace("w", self.lowerEntry_onChange)
        self.maxValueEntry = tk.Entry(sliderFrame, textvariable=self.upperBoundEntry)
        self.upperEntryString.trace("w", self.upperEntry_onChange)
        self.minValueEntry.pack()
        self.maxValueEntry.pack()

        # bind our slider state change event
        self.rangeSlider.subscribe(self.slider_changeState)
        self.slider_changeState(None)

        self.main.mainloop()



    # Function for closing
    def close(self):
        self.main.destroy()

    def slider_changeState(self, e):
        if (self.focus_displayof() != self.lowerBoundEntry):
            self.lowerBoundEntry.delete(0, END)
            self.lowerBoundEntry.insert(0, self.rangeSlider.getLowerBound())

        if (self.focus_displayof() != self.upperBoundEntry):
            self.upperBoundEntry.delete(0, END)
            self.upperBoundEntry.insert(0, self.rangeSlider.getUpperBound())




test_MainView = test_RangeSlider()
test_MainView.test_RangeSliderImpl()

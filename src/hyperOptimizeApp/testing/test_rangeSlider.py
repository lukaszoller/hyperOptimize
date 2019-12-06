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
        #self.rangeSlider.setUpperBound(1000)
        #self.rangeSlider.setLowerBound(500)
        #self.rangeSlider.setLower(650)
        #self.rangeSlider.setUpper(750)
        self.rangeSlider.configure()
        self.rangeSlider.setMajorTickSpacing(50)
        self.rangeSlider.setMinorTickSpacing(10)
        self.rangeSlider.setPaintTicks(True)
        self.rangeSlider.setSnapToTicks(False)
        self.rangeSlider.setFocus()
        self.rangeSlider.pack()

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()


test_MainView = test_RangeSlider()
test_MainView.test_RangeSliderImpl()
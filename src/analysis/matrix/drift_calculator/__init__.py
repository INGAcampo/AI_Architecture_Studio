class DriftCalculator:
    def calculate(self,top,bottom,height):
        d=top-bottom;return d,abs(d)/height

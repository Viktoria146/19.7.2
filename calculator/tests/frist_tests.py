import pytest


from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_muktiply_calculate_correctly(self):
        assert  self.calc.multiply(self, 3, 2) == 6


    def test_division_calculate_correctly(self):
        assert self.calc.division(self, 36, 6) == 6

    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(self, 10, 2) == 8

    def test_adding_calculate_correctly(self):
        assert self.calc.adding(self, 5, 4) == 9


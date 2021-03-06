import member_functions as mf
import defuzzifiers as dz
import matplotlib.pyplot as plt
import numpy as np
import sys
import random

class FuzzyInferenceSystem:
    def __init__(self):
        self.rules = [("very good approval chance","gg","go"),
                      ("good approval chance","gg"),
                      ("good approval chance","rg","go"),
                      ("regular approval chance","rg","ro"),
                      ("bad approval chance","rg","bo"),
                      ("bad approval chance","bg"),
                      ("very bad approval chance","bg","bo"),]

    def fuzzify(self, student):

        fuzzy_grade = mf.fuzzify_grade(student[0])
        fuzzy_opinion = mf.fuzzify_opinion(student[1])

        self.fuzzified = {"bg":fuzzy_grade["bad"],
                          "rg":fuzzy_grade["regular"],
                          "gg":fuzzy_grade["good"],
                          "bo":fuzzy_opinion["bad"],
                          "ro":fuzzy_opinion["regular"],
                          "go":fuzzy_opinion["good"]}

    def run_larsen(self, student, plott = False):
        print("Starting Fuzzy System using Larsen")
        self.fuzzify(student)
        self.rulify()
        if plott:
            self.plot_larsen_agregation()
        function = self.larsen_agregation
        dz.run_defuzzyfiers(function)
        return self.larsen_agregation

    def rulify(self):
        self.coeficient = {}
        for rule in self.rules:
            if not rule[0] in self.coeficient.keys():
                self.coeficient[rule[0]] = 0

            value = float(1)
            for fv in rule[1:]:
                value *= self.fuzzified[fv]

            if value > self.coeficient[rule[0]]:
                self.coeficient[rule[0]] = value
    ##### Mamdani #####
    def plot_mamdani_agregation(self):
        print("Plotting Mamdani Agregation")
        vb_coef = self.coeficient["very bad approval chance"]
        b_coef = self.coeficient["bad approval chance"]
        r_coef = self.coeficient["regular approval chance"]
        g_coef = self.coeficient["good approval chance"]
        vg_coef = self.coeficient["very good approval chance"]

        xs = np.arange(0, 100, 0.5)

        cvbys = [self.clipping(vb_coef,mf.very_bad_chance,x) for x in xs]
        cbys = [self.clipping(b_coef,mf.bad_chance,x) for x in xs]
        crys = [self.clipping(r_coef,mf.regular_chance,x) for x in xs]
        cgys = [self.clipping(g_coef,mf.good_chance,x) for x in xs]
        cvgys = [self.clipping(vg_coef,mf.very_good_chance,x) for x in xs]

        plt.plot(xs, cvbys, xs, cbys, xs, crys, xs, cgys, xs, cvgys)
        plt.title("clipped plots")
        plt.show()

        vbys = [mf.very_bad_chance(x) for x in xs]
        bys = [mf.bad_chance(x) for x in xs]
        rys = [mf.regular_chance(x) for x in xs]
        gys = [mf.good_chance(x) for x in xs]
        vgys = [mf.very_good_chance(x) for x in xs]

        plt.plot(xs, vbys, xs, bys, xs, rys, xs, gys, xs, vgys)
        plt.title("non clipped plots")
        plt.show()
        print("coeficient vals: %s, %s, %s, %s, %s" %(vb_coef, b_coef, r_coef, g_coef, vg_coef))
    def mamdani_agregation(self, chance):
        vb_coef = self.coeficient["very bad approval chance"]
        b_coef = self.coeficient["bad approval chance"]
        r_coef = self.coeficient["regular approval chance"]
        g_coef = self.coeficient["good approval chance"]
        vg_coef = self.coeficient["very good approval chance"]
        return max([self.clipping(vb_coef,mf.very_bad_chance,chance),
                    self.clipping(b_coef,mf.bad_chance,chance),
                    self.clipping(r_coef,mf.regular_chance,chance),
                    self.clipping(g_coef,mf.good_chance,chance),
                    self.clipping(vg_coef,mf.very_good_chance,chance)])
    def clipping(self, coeficient, consecuent, chance):
        return min(coeficient, consecuent(chance))

    ##### Larsen #####
    def plot_larsen_agregation(self):
        print("Plotting Larsen Agregation")
        vb_coef = self.coeficient["very bad approval chance"]
        b_coef = self.coeficient["bad approval chance"]
        r_coef = self.coeficient["regular approval chance"]
        g_coef = self.coeficient["good approval chance"]
        vg_coef = self.coeficient["very good approval chance"]

        xs = np.arange(0, 100, 0.5)

        cvbys = [self.scalate(vb_coef,mf.very_bad_chance,x) for x in xs]
        cbys = [self.scalate(b_coef,mf.bad_chance,x) for x in xs]
        crys = [self.scalate(r_coef,mf.regular_chance,x) for x in xs]
        cgys = [self.scalate(g_coef,mf.good_chance,x) for x in xs]
        cvgys = [self.scalate(vg_coef,mf.very_good_chance,x) for x in xs]

        plt.plot(xs, cvbys, xs, cbys, xs, crys, xs, cgys, xs, cvgys)
        plt.title("scaled plots")
        plt.show()

        vbys = [mf.very_bad_chance(x) for x in xs]
        bys = [mf.bad_chance(x) for x in xs]
        rys = [mf.regular_chance(x) for x in xs]
        gys = [mf.good_chance(x) for x in xs]
        vgys = [mf.very_good_chance(x) for x in xs]

        plt.plot(xs, vbys, xs, bys, xs, rys, xs, gys, xs, vgys)
        plt.title("non scaled plots")
        plt.show()
        print("coeficient vals: %s, %s, %s, %s, %s" %(vb_coef, b_coef, r_coef, g_coef, vg_coef))
    def larsen_agregation(self, chance):
        vb_coef = self.coeficient["very bad approval chance"]
        b_coef = self.coeficient["bad approval chance"]
        r_coef = self.coeficient["regular approval chance"]
        g_coef = self.coeficient["good approval chance"]
        vg_coef = self.coeficient["very good approval chance"]
        return max([self.scalate(vb_coef, mf.very_bad_chance, chance),
                    self.scalate(b_coef, mf.bad_chance, chance),
                    self.scalate(r_coef, mf.regular_chance, chance),
                    self.scalate(g_coef, mf.good_chance, chance),
                    self.scalate(vg_coef, mf.very_good_chance, chance)])
    def scalate(self, coeficient, consecuent, chance):
        return coeficient*consecuent(chance)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Uzycie: python fuzzy_inference_system.py [plots]")
        exit()
    if len(sys.argv) > 1:
        plott = True
    else:
        plott = False
    try:
        grade = float(input("Wstaw średnią ocen z przedmiotu: skala [0,5]\n>>> "))
    except:
        print("Wartość notatki musi być liczbą rzeczywistą")
        exit()

    if  not( 0 <= grade <= 5):
        print("Wstawiona notatka nie mieści się w zakresie prawidłowych wartości")
        exit()

    try:
        opinion = float(input("Wstaw opinię obsłudze wydziału na temat: skala [0,100]\n>>> "))
    except:
        print("Wartość opinii musi być liczbą rzeczywistą")
        exit()


    if  not( 0 <= opinion <= 100):
        print("Wstawiona opinia nie mieści się w zakresie prawidłowych wartości")
        exit()

    f_system = FuzzyInferenceSystem()
    student = (grade, opinion)
    f_system.run_mamdani(student, plott)
    f_system.run_larsen(student, plott)

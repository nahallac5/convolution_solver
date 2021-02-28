# libraries
import math


# Classes
class Param:
    def __init__(self, pitch, space, na_lens, wavelength):
        self.pitch = pitch
        self.space = space
        self.NA = na_lens
        self.wavelength = wavelength

    def sp_ratio(self):
        return self.space / self.pitch

    def order_mag(self, order):
        return


# Read in function for user input
def read_in():
    print("====================================================")
    print("Welcome to Orp-Lith! Please enter your parameters...")
    print("====================================================")
    accept_vars = 1

    # Get parameters from user
    while accept_vars == 1:
        # UI
        pitch = input("Pitch (nm): ")
        space = input("Space (nm): ")
        na_lens = input("NA: ")
        wavelength = input("Wavelength (nm): ")
        exit_cond = input("Is this correct?\nPitch: " + pitch + "nm\nSpace: " + space + "nm\nNA: " + na_lens + "\nWavelength: " + wavelength + "nm\n(Y or N?): ")
        if exit_cond.lower() in ["y", "yes"]:
            break

    # Store in Param class
    ui = Param(pitch, space, na_lens, wavelength)
    return ui


# Delta function filter
def delta_filter(ui):
    return

# Run
ui = read_in()

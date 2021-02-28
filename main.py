# libraries
import math


# Classes
class Param:
    # Basic Variables
    def __init__(self, pitch, space, na_lens, wavelength):
        # User input
        self.pitch = float(pitch)
        self.space = float(space)
        self.NA = float(na_lens)
        self.wavelength = float(wavelength)
        # Storage Arrays
        self.delta_mag_list = []
        self.delta_loc_list = []

    # Ratio for uneven space/line pairs
    def sp_ratio(self):
        return self.space / self.pitch

    # Gets magnitudes of the orders of delta functions
    def order_mag(self, order):
        if order == 0:
            return self.sp_ratio()
        else:
            return self.sp_ratio() * (math.sin(self.sp_ratio() * math.pi * order) / (self.sp_ratio() * math.pi * order))

    # Runs filter based on wavelength and NA
    def sin_theta(self, order):
        return (order * self.wavelength) / self.pitch


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

        # Error checking
        if space >= pitch:
            print("Space is larger than pitch. Please reenter.")
        elif float(na_lens) > 1.51:
            print("NA can not achieve a value higher than 1.51. Please reenter.")

        # Errors passed
        else:
            exit_cond = input("\nIs this correct?\nPitch: " + pitch + "nm\nSpace: " + space + "nm\nNA: " + na_lens + "\nWavelength: " + wavelength + "nm\n(Y or N?): ")
            if exit_cond.lower() in ["y", "yes"]:
                break

    # Store in Param class
    ui_init = Param(pitch, space, na_lens, wavelength)
    return ui_init


# Delta function filter
def delta_filter(ui):
    print("\nFiltering transform...\n")
    # Initial 0th order to prevent errors
    ui.delta_mag_list.append(ui.order_mag(0))
    ui.delta_loc_list.append(ui.sin_theta(0))

    # Loops order until NA filter is hit
    order = 1
    while order != -1:
        delta_loc = ui.sin_theta(order)

        # Failure condition
        if delta_loc > ui.NA:
            print("Transform filtered...\n")
            break

        # Adding next order to list
        else:
            ui.delta_mag_list.append(ui.order_mag(order))
            ui.delta_loc_list.append(ui.sin_theta(order))
            order = order + 1


# Un-transform filtered delta functions
def delta_processing(ui):
    # Get size of list for making cosine series
    terms = len(ui.delta_loc_list)


# Run
ui = read_in()
delta_filter(ui)

print(ui.delta_mag_list)
print(ui.delta_loc_list)

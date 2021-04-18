# libraries
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Classes
class Param:
    # Basic Variables
    def __init__(self, pitch, space, na_lens, wavelength, attenuation):
        # User input
        self.pitch = float(pitch)
        self.space = float(space)
        self.NA = float(na_lens)
        self.wavelength = float(wavelength)
        # HW 8 New Phase Shift
        self.attenuation = float(attenuation)
        # Storage Arrays
        self.delta_mag_list = []
        self.delta_loc_list = []

    # Ratio for uneven space/line pairs
    def sp_ratio(self):
        return self.space / self.pitch

    # Gets magnitudes of the orders of delta functions
    # Now added in attenuation shifting. At 0, this does nothing so no issue having it around all the time
    def order_mag(self, order):
        if order == 0:
            return self.sp_ratio() * (1 + np.sqrt(self.attenuation)) - np.sqrt(self.attenuation)
        else:
            return (1 + np.sqrt(self.attenuation)) * (self.sp_ratio() * (np.sin(self.sp_ratio() * np.pi * order) / (self.sp_ratio() * np.pi * order)))

    # Runs filter based on wavelength and NA
    def sin_theta(self, order):
        return (order * self.wavelength) / self.pitch

    # Returns min sigma for partial coherence
    def min_sig(self):
        min_sig = ((self.wavelength / self.pitch) - self.NA) / self.NA
        if min_sig < 0:
            return 0
        elif min_sig > 1:
            return 1
        else:
            return min_sig


# Read in function for user input
def read_in():
    accept_vars = 1

    # Get parameters from user
    while accept_vars == 1:
        # UI
        pitch = input("Pitch (nm): ")
        space = input("Space (nm): ")
        na_lens = input("NA: ")
        wavelength = input("Wavelength (nm): ")
        attenuation = input("Attenuation % (deci): ")

        # Errors passed
        #else:
        exit_cond = input("\nIs this correct?\nPitch: " + pitch + "nm\nSpace: " + space + "nm\nNA: " + na_lens + "\nWavelength: " + wavelength + "nm\nAttenuation: " + attenuation + "\n(Y or N?): ")
        if exit_cond.lower() in ["y", "yes"]:
            break

    # Store in Param class
    ui_init = Param(pitch, space, na_lens, wavelength, attenuation)
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
    print("Building intensity curves...\n")

    # Scaling setup
    u_o = 1 / ui.pitch
    x = np.arange(-1.0 * ui.pitch, 1.0 * ui.pitch, 0.01)

    # If just zero term, make an exit condition
    if len(ui.delta_loc_list) == 1:
        print(ui.delta_loc_list)
        m_prime = np.array([ui.delta_mag_list[0] for i in range(len(x))])
    
    # Building time
    else:
        # Set sympy up for x var
        x_var = sp.symbols('x')
        # Init output expression to be subbed into
        out_expression = None
        # Loop over index of all relevent vars
        for index in range(len(ui.delta_loc_list)):
            # Simple conidtion for 0 index
            if index == 0:
                out_expression = ui.delta_mag_list[index]
            # Builds equation for rest of them...
            else:
                out_expression = out_expression + 2 / index * ui.delta_mag_list[index] * sp.cos(2 * index * sp.pi * u_o * x_var)

        # Time to sub in x array
        # Lambdify allows a list to be fed into equation
        f = sp.lambdify(x_var, out_expression)
        m_prime = f(x)
    # Function plotter
    intensity = np.square(m_prime)

    # Tests on intensity plot

    # Image Contrast
    image_contrast = format((max(intensity) - min(intensity)) / (max(intensity) + min(intensity)), ".3f")

    # Image Log Slope
    mask_edge = ui.space * 0.5
    mask_edge_loc = np.searchsorted(x, mask_edge, 'left')
    dx = np.diff(x)
    dy = np.diff(np.log(intensity))
    slope = dy / dx
    ils = abs(slope[mask_edge_loc])

    # Normalized Image Log Slope
    if ui.pitch - ui.space < ui.space:
        cd = ui.pitch - ui.space
    else:
        cd = ui.space
    nils = ils * cd

    # Text for figure variables
    param_text = "Parameters:\n=======\nPitch: " + str(ui.pitch) + "nm\nSpace: " + str(ui.space) + "nm\nNA: " + str(ui.NA) + "\nλ: " + str(ui.wavelength) + "nm\nAtten: " + str(ui.attenuation) + "\n\n"
    test_text = "Tests:\n=======\nILS: " + "{:.2e}".format(ils) + "nm$^{-1}$\nNILS: " + format(nils, ".3f") + "\nImage Cont: " + str(image_contrast) + "\n\n"
    part_co_text = "Part. Coherence:\n=======\n\u03C3: " + format(ui.min_sig(), ".3f") 
    out_text = param_text + test_text + part_co_text

    # Set up figure
    fig = plt.figure()
    plt.plot(x, intensity)
    plt.xlabel('Arial distance from -' + str(ui.pitch) + 'nm to ' + str(ui.pitch) + 'nm')
    plt.ylabel('Intensity')
    plt.title('Intensity Curve')
    fig.text(.76, 0.4, out_text, ha='left')
    fig.set_size_inches(6, 6, forward=True)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75, top=0.9)
    plt.show()


# Run
def run():
    print("====================================================")
    print("Welcome to Orp-Lith! Please enter your parameters...")
    print("====================================================")
    # Will keep running until told to exit
    running = 1
    while running != -1:
        # Test Condition
        # ui = Param(260, 130, 0.75, 193)
        ui = read_in()
        delta_filter(ui)
        delta_processing(ui)

        # Exit check
        prog_loop = input("Would you like to make another chart? (Y or N): ")
        if prog_loop.lower() in ["n", "no"]:
            break


run()

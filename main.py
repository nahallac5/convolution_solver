# libraries
import matplotlib.pyplot as plt
import numpy as np


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
            return self.sp_ratio() * (np.sin(self.sp_ratio() * np.pi * order) / (self.sp_ratio() * np.pi * order))

    # Runs filter based on wavelength and NA
    def sin_theta(self, order):
        return (order * self.wavelength) / self.pitch


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

        # Error checking
        #if space >= pitch:
        #    print("Space is larger than pitch. Please reenter.")
        #elif float(na_lens) > 1.51:
        #    print("NA can not achieve a value higher than 1.51. Please reenter.")

        # Errors passed
        #else:
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
    print("Building intensity curves...\n")
    # Get size of list for making cosine series
    terms = len(ui.delta_loc_list)

    # Scaling setup
    u_o = 1 / ui.pitch
    x = np.arange(-1.0 * ui.pitch, 1.0 * ui.pitch, 0.01)
    # Function builder **This for sure can be cleaner...**
    if terms == 1:
        mag_0 = ui.delta_mag_list[0]
        m_prime = np.array([mag_0 for i in range(len(x))])
    elif terms == 2:
        mag_0 = ui.delta_mag_list[0]
        mag_1 = ui.delta_mag_list[1]
        m_prime = mag_0 + 2 * mag_1 * np.cos(2 * np.pi * u_o * x)
    elif terms == 3:
        mag_0 = ui.delta_mag_list[0]
        mag_1 = ui.delta_mag_list[1]
        mag_2 = ui.delta_mag_list[2]
        m_prime = mag_0 + 2 * mag_1 * np.cos(2 * np.pi * u_o * x) + (2/3) * mag_2 * np.cos(6 * np.pi * u_o * x)
    elif terms == 4:
        mag_0 = ui.delta_mag_list[0]
        mag_1 = ui.delta_mag_list[1]
        mag_2 = ui.delta_mag_list[2]
        mag_3 = ui.delta_mag_list[3]
        m_prime = mag_0 + 2 * mag_1 * np.cos(2 * np.pi * u_o * x) + (2/3) * mag_2 * np.cos(6 * np.pi * u_o * x) + (2/5) * mag_3 * np.cos(10 * np.pi * u_o * x)
    elif terms == 5:
        mag_0 = ui.delta_mag_list[0]
        mag_1 = ui.delta_mag_list[1]
        mag_2 = ui.delta_mag_list[2]
        mag_3 = ui.delta_mag_list[3]
        mag_4 = ui.delta_mag_list[4]
        m_prime = mag_0 + 2 * mag_1 * np.cos(2 * np.pi * u_o * x) + (2/3) * mag_2 * np.cos(6 * np.pi * u_o * x) + (2/5) * mag_3 * np.cos(10 * np.pi * u_o * x) + (2/7) * mag_4 * np.cos(14 * np.pi * u_o * x)
    else:
        m_prime = np.array([.5 for i in range(len(x))])

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
    param_text = "Parameters:\n=======\nPitch: " + str(ui.pitch) + "nm\nSpace: " + str(ui.space) + "nm\nNA: " + str(ui.NA) + "\nλ: " + str(ui.wavelength) + "nm\n\n"
    test_text = "Tests:\n=======\nILS: " + "{:.2e}".format(ils) + "nm$^{-1}$\nNILS: " + format(nils, ".3f") + "\nImage Cont: " + str(image_contrast)
    out_text = param_text + test_text

    # Set up figure
    fig = plt.figure()
    plt.plot(x, intensity)
    plt.xlabel('Arial distance from -' + str(ui.pitch) + 'nm to ' + str(ui.pitch) + 'nm')
    plt.ylabel('Intensity')
    plt.title('Intensity Curve')
    fig.text(.76, 0.5, out_text, ha='left')
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

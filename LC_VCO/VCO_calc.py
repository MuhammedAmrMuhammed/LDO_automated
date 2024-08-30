import tkinter as tk
from tkinter import ttk
from math import pi
#from PIL import Image, ImageTk

def calculate_missing_parameter():
    try:
        L_nH = entry_L.get()
        C_pF = entry_C.get()
        f_value = entry_f.get()

        if not L_nH and C_pF and f_value:
            f_Hz = convert_to_hz(float(f_value), frequency_unit.get())
            C = float(C_pF) * 1e-12  # Convert pF to F
            L = 1 / (4 * pi**2 * f_Hz**2 * C)
            L_nH = L * 1e9  # Convert H to nH
            label_result.set(f"Calculated Inductance: {L_nH:.2f} nH")
            entry_L.insert(0, f"{L_nH:.2f}")
        elif not C_pF and L_nH and f_value:
            f_Hz = convert_to_hz(float(f_value), frequency_unit.get())
            L = float(L_nH) * 1e-9  # Convert nH to H
            C = 1 / (4 * pi**2 * f_Hz**2 * L)
            C_pF = C * 1e12  # Convert F to pF
            label_result.set(f"Calculated Capacitance: {C_pF:.2f} pF")
            entry_C.insert(0, f"{C_pF:.2f}")
        elif not f_value and L_nH and C_pF:
            L = float(L_nH) * 1e-9  # Convert nH to H
            C = float(C_pF) * 1e-12  # Convert pF to F
            frequency = 1 / (2 * pi * sqrt(L * C))
            unit = frequency_unit.get()
            if unit == "Hz":
                frequency_converted = frequency
            elif unit == "kHz":
                frequency_converted = frequency / 1e3
            elif unit == "MHz":
                frequency_converted = frequency / 1e6
            elif unit == "GHz":
                frequency_converted = frequency / 1e9
            label_result.set(f"Calculated Frequency: {frequency_converted:.2f} {unit}")
            entry_f.insert(0, f"{frequency_converted:.2f}")
        else:
            label_result.set("Please leave exactly one field empty for calculation.")
    except ValueError:
        label_result.set("Invalid input. Please enter numeric values.")

def calculate_gm():
    try:
        Rp = float(entry_Rp.get())
        gm = 1 / Rp
        label_result_gm.config(text=f"Required gm: {gm:.2f} S")
    except ValueError:
        label_result_gm.config(text="Invalid input. Please enter a numeric value.")

def calculate_phase_noise():
    try:
        k = 1.38e-23  # Boltzmann constant in J/K
        T = float(entry_T.get())  # Temperature in Kelvin
        gamma = float(entry_gamma.get())  # Noise factor
        ISS = float(entry_ISS.get())  # Bias current in mA
        V0 = float(entry_V0.get())  # Oscillation amplitude in V
        f0 = convert_to_hz(float(entry_f0.get()), frequency_unit_phase.get())  # Oscillation frequency in Hz
        Q = float(entry_Q.get())  # Quality factor
        delta_f = float(entry_delta_f.get())  # Offset frequency in Hz

        phase_noise = (2 * pi * k * T * (gamma + 1)) / ((ISS*1e-3) * V0) * (f0 / (2 * Q * delta_f))
        phase_noise_result.set(f"Phase Noise: {phase_noise:.2e} dBc/Hz")
    except ValueError:
        phase_noise_result.set("Invalid input. Please enter numeric values.")

def convert_to_hz(frequency, unit):
    if unit == "Hz":
        return frequency
    elif unit == "kHz":
        return frequency * 1e3
    elif unit == "MHz":
        return frequency * 1e6
    elif unit == "GHz":
        return frequency * 1e9

root = tk.Tk()
root.title("LC VCO Calculator")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="LC VCO Calculator")

label_L = tk.Label(tab1, text="Inductance (L) in nH:")
label_L.pack()
entry_L = tk.Entry(tab1)
entry_L.pack()

label_C = tk.Label(tab1, text="Capacitance (C) in pF:")
label_C.pack()
entry_C = tk.Entry(tab1)
entry_C.pack()

label_f = tk.Label(tab1, text="Frequency (f):")
label_f.pack()
entry_f = tk.Entry(tab1)
entry_f.pack()

frequency_unit = tk.StringVar(value="Hz")
label_unit = tk.Label(tab1, text="Select Frequency Unit:")
label_unit.pack()
unit_menu = tk.OptionMenu(tab1, frequency_unit, "Hz", "kHz", "MHz", "GHz")
unit_menu.pack()

label_Rp = tk.Label(tab1, text="Equivalent Parallel Resistance (Rp) in Ohms:")
label_Rp.pack()
entry_Rp = tk.Entry(tab1)
entry_Rp.pack()

button_calculate = tk.Button(tab1, text="Calculate", command=calculate_missing_parameter)
button_calculate.pack()

button_gm = tk.Button(tab1, text="Calculate gm", command=calculate_gm)
button_gm.pack()

label_result = tk.StringVar()
label_result.set("")
result_label = tk.Label(tab1, textvariable=label_result)
result_label.pack()

label_result_gm = tk.Label(tab1, text="")
label_result_gm.pack()


tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Phase Noise")


label_T = tk.Label(tab2, text="Temperature (T) in Kelvin:")
label_T.pack()
entry_T = tk.Entry(tab2)
entry_T.pack()

label_gamma = tk.Label(tab2, text="Noise Factor (γ):")
label_gamma.pack()
entry_gamma = tk.Entry(tab2)
entry_gamma.pack()

label_ISS = tk.Label(tab2, text="Bias Current (I_SS) in mA:")
label_ISS.pack()
entry_ISS = tk.Entry(tab2)
entry_ISS.pack()

label_V0 = tk.Label(tab2, text="Oscillation Amplitude (V_0) in V:")
label_V0.pack()
entry_V0 = tk.Entry(tab2)
entry_V0.pack()

label_f0 = tk.Label(tab2, text="Oscillation Frequency (f_0):")
label_f0.pack()
entry_f0 = tk.Entry(tab2)
entry_f0.pack()

# Dropdown menu for frequency units in tab2
frequency_unit_phase = tk.StringVar(value="Hz")
label_unit_phase = tk.Label(tab2, text="Select Frequency Unit for f_0:")
label_unit_phase.pack()
unit_menu_phase = tk.OptionMenu(tab2, frequency_unit_phase, "Hz", "kHz", "MHz", "GHz")
unit_menu_phase.pack()

label_Q = tk.Label(tab2, text="Quality Factor (Q):")
label_Q.pack()
entry_Q = tk.Entry(tab2)
entry_Q.pack()

label_delta_f = tk.Label(tab2, text="Offset Frequency (Δf) in Hz:")
label_delta_f.pack()
entry_delta_f = tk.Entry(tab2)
entry_delta_f.pack()


button_phase_noise = tk.Button(tab2, text="Calculate Phase Noise", command=calculate_phase_noise)
button_phase_noise.pack()

phase_noise_result = tk.StringVar()
phase_noise_result.set("")
result_phase_noise = tk.Label(tab2, textvariable=phase_noise_result)
result_phase_noise.pack()


root.mainloop()

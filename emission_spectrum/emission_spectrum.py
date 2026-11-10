import os 
import numpy as np
import re

def read_values(file_name: str) -> dict:
    """
    Read the text files and create a dictionary.
    Uses regular expressions to separate color names with spaces and their angles.
    Returns: {'MORADO TENUE': (7.0, 30.0, 0.0), ...}
    """
    data_dict = {}
    filepath = os.path.join("data", file_name)
    
    # Regular expression pattern to match the color name and angles in DMS format
    # Example: "MORADO TENUE 7°30'" -> Group 1: "MORADO TENUE", Group 2: "7", Group 3: "30"
    pattern = re.compile(r"^(.*?)\s+([\d\.]+)°([\d\.]+)'")

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.search(line)
            if match:
                color = match.group(1).strip()
                d = float(match.group(2))
                m = float(match.group(3))
                data_dict[color] = (d, m, 0.0) # Se asume 0 segundos
                
    return data_dict 

def dms_to_degrees(d: float, m: float, s: float) -> float:
    sign = -1 if np.signbit(d) else 1
    d = abs(d)
    return sign * (d + m/60 + s/3600)

def bragg_for_grid(theta: float, n: int = 1, d: float = 282e-12):
    """
    Calculate the wavelength using Bragg's law.
    theta: Angle in degrees
    n: Order of diffraction (default is 1)
    d: Spacing between planes/slits in meters
    """
    theta_rad = np.radians(theta)  # Convert angle to radians
    wavelength = (d * np.sin(theta_rad)) / n  # Bragg's law formula
    return wavelength * 1e9  # Return wavelength in nanometers

def relative_error(measured: float, true: float) -> float:
    error = (abs(measured - true) / true) * 100
    return error

def main():
    # Theorical wavelenghts in the visible spectrum (nanometers)
    # Resource: NIST Atomic Spectra Database (https://physics.nist.gov/PhysRefData/ASD/lines_form.html)
    theoretical_data = {
        "mercury": [435.8, 435.8, 491.6, 496.0, 546.1, 577.0, 579.1, 615.0, 690.7],
        "helium": [447.1, 471.3, 492.2, 501.6, 587.6, 667.8, 706.5],
        "hydrogen": [434.0, 486.1, 656.3]
    }

    gasses = ["mercury", "helium", "hydrogen"]
    
    # Create the file to save the results
    os.makedirs("results", exist_ok=True)

    # 300 lines per mm, so the spacing between slits is 1/300 mm = 1/300 * 1e-3 m = 3.333e-6 m
    d_spacing = 3333.3e-9  # Convert to meters

    with open("results/emission_spectrum_results.txt", "w", encoding="utf-8") as fout:
        fout.write("\t--- Emission Spectrum Results ---\n\n")

        for gas in gasses:
            file_name = f"{gas}_spectrum_data.txt"
            gas_data = read_values(file_name)
                
            fout.write(f"=== GAS: {gas.upper()} ===\n")
            fout.write(f"{'Observed color':<20} | {'Angle (°)':<10} | {'Exp (nm)':<10} | {'Theoretical (nm)':<12} | {'Error (%)'}\n")
            fout.write("-" * 75 + "\n")
            
            for i, (color, (d, m, s)) in enumerate(gas_data.items()):                
                # 1. Convert DMS to decimal degrees
                theta_deg = dms_to_degrees(d, m, s)
                
                # 2. Calculates the experimental wavelength using Bragg's law
                wl_exp = bragg_for_grid(theta=theta_deg, n=1, d=d_spacing)
                
                # 3. Finds the closest theoretical wavelength for the given gas
                theor = theoretical_data[gas][i]
                
                # 4. Calculates the relative error
                error = relative_error(wl_exp, theor)
                
                # 5. Writes the results
                fout.write(f"{color:<20} | {theta_deg:<10.4f} | {wl_exp:<10.2f} | {theor:<12.2f} | {error:.2f}%\n")
                
            fout.write("\n")

    print("Results were successfully calculated and saved in the 'results/emission_spectrum_results.txt' file.")

if __name__ == "__main__":
    main()
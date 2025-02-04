from DEWPython.DEWModel import DEW
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def run_aqueous_model():
    try:
        # Create DEW model instance
        print("Initializing DEW model...")
        model = DEW()
        
        # Define aqueous species inputs with ionic components
        aq_inputs = [
            # Combined K+ from both KOH (0.5M) and K2CO3 (0.4M) = 0.9M total
            ["K+", 3],              # Total K+ (1 from KOH + 2 from K2CO3)
            
            # OH- from 0.5M KOH
            ["OH-", 1],             # From 0.5M KOH
            
            # CO3^2- from 0.2M K2CO3
            ["CO3-2", 1],           # From 0.2M K2CO3
            
            # 0.3M acetic acid
            ["ACETATE,AQ", 1]       # 0.3M acetic acid
        ]
        
        print("Running model with temperature and pressure points from input.csv...")
        # Run the model without built-in plotting
        model.run(
            pt_arr=[],  # Empty since using Custom input
            aq_inp=aq_inputs,
            ptInp='Custom',  # Use Custom to read from input.csv
            rhoWat='Z&D 2005',
            makeP=False  # Don't use built-in plotting
        )
        
        # Print debug information
        print("\nDebug Information:")
        print(f"Number of temperature points: {len(model.tempUsed)}")
        print(f"Number of pressure points: {len(model.pressureUsed)}")
        print(f"Temperature range: {min(model.tempUsed):.1f}°C to {max(model.tempUsed):.1f}°C")
        print(f"Pressure range: {min(model.pressureUsed):.1f} to {max(model.pressureUsed):.1f} bar")
        
        # Write results to CSV
        output_file = 'dew_model_results.csv'
        print(f"\nWriting results to {output_file}...")
        
        try:
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write reaction information
                writer.writerow(['Reaction Components'])
                writer.writerow(['Input Species:'])
                for species, coeff in model.aqueousInputs:
                    writer.writerow([f"{coeff} {species}"])
                writer.writerow(['Output Species:'])
                for species, coeff in model.aqueousOutputs:
                    writer.writerow([f"{coeff} {species}"])
                writer.writerow([])  # Empty row for separation
                
                # Write thermodynamic data
                headers = [
                    'Temperature (C)', 'Pressure (bar)',
                    'LogK', 'DeltaG (cal/mol)', 'DeltaV (cm3/mol)',
                    'Water Density (g/cm3)', 'Dielectric Constant'
                ]
                writer.writerow(headers)
                
                # Write data for each point
                for i in range(len(model.tempUsed)):
                    row = [
                        f"{model.tempUsed[i]:.2f}",
                        f"{model.pressureUsed[i]:.2f}",
                        f"{model.logK[i][0]:.4f}",
                        f"{model.delG[i][0]:.4f}",
                        f"{model.delV[i][0]:.4f}",
                        f"{model.RhoWatArr[i]:.6f}",
                        f"{model.DiaArr[i]:.6f}"
                    ]
                    writer.writerow(row)
            
            print(f"Results successfully written to {output_file}")
            
        except Exception as e:
            print(f"Error writing to CSV: {str(e)}")
            print("Stack trace:")
            import traceback
            traceback.print_exc()

        # Print results to console
        print("\nResults at each temperature and pressure point:")
        for i in range(len(model.tempUsed)):
            print(f"\nT = {model.tempUsed[i]}°C, P = {model.pressureUsed[i]} bar")
            print(f"LogK = {model.logK[i][0]:.4f}")
            print(f"ΔG = {model.delG[i][0]:.4f} cal/mol")
            print(f"ΔV = {model.delV[i][0]:.4f} cm³/mol")

        # Create our own plots
        print("\nGenerating plots...")
        
        # Extract data for plotting
        temperatures = model.tempUsed
        logk_values = [x[0] for x in model.logK]
        delg_values = [x[0] for x in model.delG]
        delv_values = [x[0] for x in model.delV]
        
        # Create temperature plots
        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, logk_values, 'b-', label='LogK')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('LogK')
        plt.title('LogK vs Temperature')
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, delg_values, 'r-', label='ΔG')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('ΔG (cal/mol)')
        plt.title('ΔG vs Temperature')
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, delv_values, 'g-', label='ΔV')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('ΔV (cm³/mol)')
        plt.title('ΔV vs Temperature')
        plt.grid(True)
        plt.legend()
        plt.show()

        print("Plots generated successfully")

    except Exception as e:
        print(f"Error running model: {str(e)}")
        print("Stack trace:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_aqueous_model()
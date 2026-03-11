import subprocess
import matplotlib.pyplot as plt
import csv

# Assignment parameters
error_units = ['Packet', 'Bit', 'Byte']
error_rates = [0.2, 0.4, 0.6, 0.8, 1.0]
# Your roll number ends in 50, so seeds are 50 to 59
rng_runs = list(range(50, 60)) 

def run_ns3(error_rate, error_unit, rng_run):
    cmd = f'./ns3 run "scratch/partB --errorRate={error_rate} --errorUnit={error_unit} --rngRun={rng_run}"'
    try:
        # Run the command and capture standard output
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        
        # The PDR is the last line of the standard output
        output_lines = result.stdout.strip().split('\n')
        
        # Find the last line that can be converted to a float (ignoring any stray ninja build lines)
        for line in reversed(output_lines):
            try:
                pdr = float(line)
                return pdr
            except ValueError:
                continue
        return 0.0
    except Exception as e:
        print(f"Error running NS-3 for ER={error_rate}, Unit={error_unit}, Seed={rng_run}: {e}")
        return 0.0

# Main automation loop
for unit in error_units:
    print(f"\n--- Running simulations for Error Unit: {unit} ---")
    
    # Prepare table structure
    table_data = []
    header = ["RngRun/Error Rate", "ER1=0.2", "ER2=0.4", "ER3=0.6", "ER4=0.8", "ER5=1.0"]
    table_data.append(header)
    
    # Dictionary to store PDRs to calculate the average later
    unit_pdr_results = {er: [] for er in error_rates}
    
    for i, seed in enumerate(rng_runs):
        row = [f"RngRun{i+1}={seed}"]
        print(f"Running Seed {seed} for {unit}...", end="", flush=True)
        for er in error_rates:
            pdr = run_ns3(er, unit, seed)
            row.append(f"{pdr:.5f}")
            unit_pdr_results[er].append(pdr)
        table_data.append(row)
        print(" Done.")
        
    # Calculate Averages for the final row
    avg_row = ["AVG. PDR"]
    avg_pdrs = []
    for er in error_rates:
        avg = sum(unit_pdr_results[er]) / len(rng_runs)
        avg_row.append(f"{avg:.5f}")
        avg_pdrs.append(avg)
    table_data.append(avg_row)
    
    # Save the table to a CSV file
    csv_filename = f"PDR_Table_{unit}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table_data)
    print(f"Saved table to {csv_filename}")
    
    # Plot Average PDR vs Error Rate
    plt.figure(figsize=(8, 5))
    plt.plot(error_rates, avg_pdrs, marker='o', linestyle='-', color='purple')
    plt.title(f'Average PDR vs Error Rate ({unit} Error Model)')
    plt.xlabel('Error Rate')
    plt.ylabel('Average Packet Delivery Ratio (PDR)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(error_rates)
    plt.ylim(0, 1.1)
    
    plot_filename = f"Avg_PDR_vs_ER_{unit}.png"
    plt.savefig(plot_filename)
    plt.close()
    print(f"Saved plot to {plot_filename}")

print("\nAll Part B simulations and deliverables successfully generated!")

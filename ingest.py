import os
import subprocess  # 1. ADDED THIS

def parse_and_generate_sql(input_file="clean_telemetry.csv"):
    print("Starting Python Dynamic Ingestion Layer...")
    
    # 2. ADDED THIS BLOCK TO RUN THE C PROGRAM AUTOMATICALLY
    print("Launching C Engine to gather fresh telemetry data...")
    try:
        # This is the line running the C program!
        subprocess.run(["./parser"], check=True) 
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Pipeline Error: Failed to execute C Engine. Details: {e}")
        return

    # Your original code continues here safely...
    if not os.path.exists(input_file):
        print(f"Error: Target file '{input_file}' not found. Run C engine first.")
        return

    try:
        with open(input_file, "r") as file:
            lines = file.readlines()
            
        data_lines = lines[1:]
        
        print(f"Detected {len(data_lines)} data rows. Generating DML insertions:")
        print("-" * 60)
        
        for line in data_lines:
            cleaned_line = line.strip()
            
            if not cleaned_line:
                continue
                
            row = cleaned_line.split(",")
            packet_id, lat, lon, reading = row[0], row[1], row[2], row[3]
            
            sql_query = f"INSERT INTO satellite_telemetry (packet_id, latitude, longitude, sensor_reading) VALUES ('{packet_id}', {lat}, {lon}, {reading});"
            print(sql_query)
            
        print("-" * 60)
        print("Data Ingestion Cycle Complete.")
        
    except IOError as e:
        print(f"System File Error: {e}")

if __name__ == "__main__":
    parse_and_generate_sql()

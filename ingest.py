import os

# Simulating the clean data output from our C parser engine
clean_telemetry_payload = [
    {"packet_id": 101, "lat": 12.97, "lon": 77.59, "reading": 24.5},
    {"packet_id": 103, "lat": 12.99, "lon": 77.61, "reading": 26.1},
    {"packet_id": 105, "lat": 13.01, "lon": 77.63, "reading": 23.8}
]

def log_telemetry_data(payload, filename="clean_telemetry.log"):
    print("Starting Python Telemetry Ingestion Layer...")
    print(f"Target destination log file: {filename}")
    print("-" * 50)
    
    # Utilizing core Python file handling to write data structures
    try:
        with open(filename, "w") as file:
            # Writing structured header columns for standard data engineering formats
            file.write("PACKET_ID,LATITUDE,LONGITUDE,SENSOR_READING\n")
            
            for packet in payload:
                log_line = f"{packet['packet_id']},{packet['lat']},{packet['lon']},{packet['reading']}\n"
                file.write(log_line)
                print(f"Successfully ingested and written Packet ID: {packet['packet_id']}")
                
        print("-" * 50)
        print("Data Ingestion Cycle Complete. Log file generated successfully.")
        
    except IOError as e:
        print(f"System Error: Unable to complete file operations. Detail: {e}")

if __name__ == "__main__":
    log_telemetry_data(clean_telemetry_payload)

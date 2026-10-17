
import os
import subprocess

def parse_and_generate_sql(input_file="clean_telemetry.csv"):
    print("Starting Python Dynamic Ingestion Layer...")

    # Run from the directory containing this Python file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    c_source = os.path.join(base_dir, "parser.c")
    executable = os.path.join(base_dir, "parser")
    input_file = os.path.join(base_dir, input_file)

    print("Launching C Engine to gather fresh telemetry data...")

    try:
        # Compile the C source if the executable doesn't exist
        if not os.path.exists(executable):
            print("Compiled C Engine not found. Compiling parser.c...")
            subprocess.run(
                ["gcc", c_source, "-o", executable],
                check=True,
                cwd=base_dir
            )

        # Remove old output so stale data cannot be reused
        if os.path.exists(input_file):
            os.remove(input_file)

        # Run the C program
        subprocess.run(
            [executable],
            check=True,
            cwd=base_dir
        )

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Pipeline Error: Failed to compile or execute C Engine. Details: {e}")
        return

    if not os.path.exists(input_file):
        print(f"Error: Target file '{input_file}' not found.")
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

            if len(row) != 4:
                print(f"Skipping malformed CSV row: {cleaned_line}")
                continue

            packet_id, lat, lon, reading = row

            sql_query = (
                "INSERT INTO satellite_telemetry "
                "(packet_id, latitude, longitude, sensor_reading) "
                f"VALUES ({packet_id}, {lat}, {lon}, {reading});"
            )
            print(sql_query)

        print("-" * 60)
        print("Data Ingestion Cycle Complete.")

    except IOError as e:
        print(f"System File Error: {e}")

if __name__ == "__main__":
    parse_and_generate_sql()

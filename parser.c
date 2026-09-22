#include <stdio.h>
#include <stdlib.h>

#define MAX_RECORDS 6
#define HARDWARE_SENTINEL -9999.0
#define TEMP_MIN -40.0
#define TEMP_MAX 85.0

// Structure modeling raw satellite sensor data frames
typedef struct {
    int packet_id;
    float latitude;
    float longitude;
    float sensor_reading; // Raw ambient surface temperature stream
} TelemetryPacket;

// Function to parse, validate, and isolate valid sensor entries
void process_telemetry(TelemetryPacket data[], int size) {
    printf("Initializing Telemetry Processing Engine Stream Analysis...\n");
    printf("----------------------------------------------------------\n");
    
    int valid_count = 0;
    int corrupted_count = 0;
    float rolling_sum = 0.0;

    for (int i = 0; i < size; i++) {
        // Validation Layer 1: Filter out hardware transmission sentinel values (-9999.0)
        if (data[i].sensor_reading == HARDWARE_SENTINEL) {
            printf("[PACKET %03d ALERT] Hardware Failure Detected -- Sentinel Code Found -- Dropping Frame\n", data[i].packet_id);
            corrupted_count++;
            continue;
        }

        // Validation Layer 2: Check against physical safe operating thresholds of electronic components
        if (data[i].sensor_reading < TEMP_MIN || data[i].sensor_reading > TEMP_MAX) {
            printf("[PACKET %03d ALERT] Boundary Violation: %.2f C -- Value Out of Bounds -- Dropping Frame\n", data[i].packet_id, data[i].sensor_reading);
            corrupted_count++;
            continue;
        }

        // Processing Layer: Handle clean data structures
        rolling_sum += data[i].sensor_reading;
        valid_count++;
    }

    // Output final analytical breakdown profile
    printf("----------------------------------------------------------\n");
    printf("Processing Cycle Complete.\n");
    printf("Total Packets Analyzed: %d\n", size);
    printf("Valid Frames Ingested:  %d\n", valid_count);
    printf("Corrupted Frames Split: %d\n", corrupted_count);
    
    if (valid_count > 0) {
        printf("Computed Stream Mean:   %.2f C\n", rolling_sum / valid_count);
    } else {
        printf("Warning: No valid data payloads remained after parser filtration.\n");
    }
}

int main() {
    // Simulating a messy laboratory stream containing clean steps, extreme boundaries, and missing packets
    TelemetryPacket raw_stream[MAX_RECORDS] = {
        {101, 12.97, 77.59, 24.5},    // Valid frame
        {102, 12.98, 77.60, -9999.0}, // NASA/ISRO Missing Data Sentinel Value
        {103, 12.99, 77.61, 26.1},    // Valid frame
        {104, 13.00, 77.62, 115.0},   // Component Boundary Error (>85.0 C)
        {105, 13.01, 77.63, 23.8},    // Valid frame
        {106, 13.02, 77.64, -9999.0}  // NASA/ISRO Missing Data Sentinel Value
    };

    process_telemetry(raw_stream, MAX_RECORDS);

    return 0;
}

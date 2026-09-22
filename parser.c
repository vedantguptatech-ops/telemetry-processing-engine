#include <stdio.h>
#include <stdlib.h>

#define MAX_RECORDS 6
#define HARDWARE_SENTINEL -9999.0
#define TEMP_MIN -40.0
#define TEMP_MAX 85.0

typedef struct {
    int packet_id;
    float latitude;
    float longitude;
    float sensor_reading;
} TelemetryPacket;

void process_and_export_telemetry(TelemetryPacket data[], int size, const char *output_filename) {
    FILE *file = fopen(output_filename, "w");
    if (file == NULL) {
        printf("Error: Unable to create export file.\n");
        return;
    }

    fprintf(file, "packet_id,latitude,longitude,sensor_reading\n");
    int valid_count = 0;

    for (int i = 0; i < size; i++) {
        // Drop frames matching the aerospace hardware missing data flag
        if (data[i].sensor_reading == HARDWARE_SENTINEL) continue;

        // Isolate thermal anomalies outside component data sheet limits
        if (data[i].sensor_reading < TEMP_MIN || data[i].sensor_reading > TEMP_MAX) continue;

        fprintf(file, "%d,%.2f,%.2f,%.2f\n", 
                data[i].packet_id, data[i].latitude, data[i].longitude, data[i].sensor_reading);
        
        valid_count++;
    }

    fclose(file);
    printf("C Engine Complete: Exported %d clean packets to '%s'.\n", valid_count, output_filename);
}

int main() {
    TelemetryPacket raw_stream[MAX_RECORDS] = {
        {101, 12.97, 77.59, 24.5},
        {102, 12.98, 77.60, -9999.0}, 
        {103, 12.99, 77.61, 26.1},
        {104, 13.00, 77.62, 115.0},  
        {105, 13.01, 77.63, 23.8},
        {106, 13.02, 77.64, -9999.0}  
    };

    process_and_export_telemetry(raw_stream, MAX_RECORDS, "clean_telemetry.csv");
    return 0;
}

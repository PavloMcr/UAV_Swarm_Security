import serial

# Define the allowed threshold values for RSSI and SNR
RSSI_THRESHOLD = -100  # Example threshold for RSSI
SNR_THRESHOLD = 0    # Example threshold for SNR

# Variables for sequence checking
expected_sequence = 0

def process_telemetry(telemetry, sequence):
    global expected_sequence

    rssi_index = telemetry.find("RSSI:")
    snr_index = telemetry.find("SNR:")

    if rssi_index != -1 and snr_index != -1:
        rssi_str = telemetry[rssi_index + len("RSSI:"):snr_index].strip()
        snr_str = telemetry[snr_index + len("SNR:"):].strip()

        try:
            rssi = int(rssi_str)
            snr = int(snr_str)

            # Compare with the thresholds
            if rssi < RSSI_THRESHOLD or snr < SNR_THRESHOLD:
                print("Possible jamming attack detected!")
            else:
                print("Telemetry received. RSSI:", rssi, "SNR:", snr)

            # Check sequence number
            if sequence != expected_sequence:
                print("Unexpected sequence number. Possible jamming attack!")
            else:
                expected_sequence += 1

        except ValueError:
            print("Error parsing telemetry data.")

# Serial communication with ESP32
ser = serial.Serial('/dev/ttyS0', 115200)  # Adjust the port and baud rate accordingly

try:
    while True:
        telemetry = ser.readline().decode('utf-8').strip()
        if telemetry.startswith("Telemetry:"):
            sequence_str = telemetry[len("Telemetry:"):].split()[0]
            sequence = int(sequence_str)
            process_telemetry(telemetry[len("Telemetry:"):], sequence)

except KeyboardInterrupt:
    ser.close()
    print("Script terminated.")

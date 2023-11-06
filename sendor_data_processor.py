class SensorDataProcessor:
    def __init__(self, sensor_interface):
        self.sensor_interface = sensor_interface
        self.latest_data = {}

    def update_sensor_data(self):
        """Retrieve the latest data from sensors and update internal state."""
        raw_data = self.sensor_interface.read_all_sensors()
        self.latest_data = self.process_raw_data(raw_data)

    def process_raw_data(self, raw_data):
        """Process raw data from sensors into a more usable form."""
        processed_data = {}
        # Implement the processing of raw data for each sensor.
        # This could involve calibrations, unit conversions, filtering, etc.
        for sensor_id, data in raw_data.items():
            # As an example, let's assume we need to convert raw accelerometer
            # data into a measure of tilt in degrees.
            if sensor_id.startswith('accel'):
                processed_data[sensor_id] = self.convert_accel_to_tilt(data)
            elif sensor_id.startswith('gyro'):
                # Similarly, process gyroscope data
                processed_data[sensor_id] = self.process_gyro_data(data)
            # ... handle other sensor types as necessary

        return processed_data

    def convert_accel_to_tilt(self, accel_data):
        """Convert raw accelerometer data to tilt angles."""
        # Implement the conversion logic
        tilt_angles = {}
        # Assuming accel_data is a dictionary with keys 'x', 'y', 'z'
        # and these are raw accelerometer readings.
        # The following is a simplified example of calculating tilt.
        tilt_angles['x'] = self.calculate_tilt(accel_data['x'])
        tilt_angles['y'] = self.calculate_tilt(accel_data['y'])
        tilt_angles['z'] = self.calculate_tilt(accel_data['z'])
        return tilt_angles

    def calculate_tilt(self, accel_value):
        """Calculate the tilt angle from a single axis accelerometer value."""
        # Placeholder for actual calculation:
        return accel_value * 90  # Simplified example

    def process_gyro_data(self, gyro_data):
        """Process gyroscope data."""
        # Implement the processing of gyroscope data
        # This could involve unit conversions or filtering.
        processed_gyro = {}
        # Assuming gyro_data is a dictionary with keys 'x', 'y', 'z'
        # and these are raw gyroscope readings.
        processed_gyro['x'] = gyro_data['x'] * (180 / 32768)  # Example conversion
        processed_gyro['y'] = gyro_data['y'] * (180 / 32768)
        processed_gyro['z'] = gyro_data['z'] * (180 / 32768)
        return processed_gyro

    def get_latest_data(self):
        """Return the latest processed sensor data."""
        return self.latest_data

# Example usage:
# Assuming you have a sensor interface that can read all sensors.
sensor_interface = SensorInterface()  # Placeholder for your sensor interface class or library.
sensor_processor = SensorDataProcessor(sensor_interface)

# Regularly update sensor data.
sensor_processor.update_sensor_data()

# Get the latest processed sensor data.
latest_data = sensor_processor.get_latest_data()
print(latest_data)

class RobotState:
    def __init__(self):
        # Position could be in 2D or 3D space depending on the robot
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        # Orientation could be represented as Euler angles, a quaternion, etc.
        self.orientation = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}
        # Velocity and angular velocity
        self.velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.angular_velocity = {'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0}
        # Status of actuators (for simplicity, represented as angles for servos)
        self.actuator_states = {'servo1': 0.0, 'servo2': 0.0, ...}
        # Sensor readings (could include IR, ultrasonic, touch sensors, etc.)
        self.sensor_readings = {'sensor1': 0.0, 'sensor2': 0.0, ...}
        # Other states can be added as needed for the robot

    def update_position(self, new_position):
        self.position.update(new_position)

    def update_orientation(self, new_orientation):
        self.orientation.update(new_orientation)

    def update_velocity(self, new_velocity):
        self.velocity.update(new_velocity)

    def update_angular_velocity(self, new_angular_velocity):
        self.angular_velocity.update(new_angular_velocity)

    def update_actuator_state(self, actuator_id, new_state):
        self.actuator_states[actuator_id] = new_state

    def update_sensor_reading(self, sensor_id, new_reading):
        self.sensor_readings[sensor_id] = new_reading

    def get_state(self):
        # Return a dictionary of the current state
        return {
            'position': self.position,
            'orientation': self.orientation,
            'velocity': self.velocity,
            'angular_velocity': self.angular_velocity,
            'actuator_states': self.actuator_states,
            'sensor_readings': self.sensor_readings
        }

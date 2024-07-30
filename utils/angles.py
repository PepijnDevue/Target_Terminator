import numpy as np
import matplotlib.pyplot as plt

def calculate_angle_difference(
    position: np.ndarray, 
    target_position: np.ndarray, 
    unit_velocity_vector: np.ndarray, 
):
    # Step 1: Calculate the direction vector to the target
    direction_to_target = target_position - position
    
    # Normalize the direction vector to the target
    unit_vector_to_target = direction_to_target / np.linalg.norm(direction_to_target)
    print(unit_vector_to_target)
    
    # Step 2: Calculate the dot product of the two unit vectors
    return np.dot(unit_vector_to_target, unit_velocity_vector)

# Example usage:
position = np.array([0, 360])
target_position = np.array([0, 500])
velocity_vector = np.array([10.0, 0.0])

# Normalize the velocity vector to get the unit velocity vector
unit_velocity_vector = velocity_vector / np.linalg.norm(velocity_vector)

angle_diff_clipped = calculate_angle_difference(position, target_position, unit_velocity_vector)
print(f"Clipped angle difference: {angle_diff_clipped}")

def rotate_number(A):
    if -1 <= A <= 1:
        # Calculate the angle in radians
        theta = A * (np.pi / 2)
        # Calculate B using the cosine function
        B = np.cos(theta)
        return B
    else:
        raise ValueError("Input A must be between -1 and 1")
    
print(f"Cosine of angle differen: {np.degrees(np.arccos(angle_diff_clipped))}")

plt.plot(position)
plt.plot(target_position)
plt.quiver(*position, *unit_velocity_vector, angles='xy', scale_units='xy', scale=1, color='r')
plt.show()
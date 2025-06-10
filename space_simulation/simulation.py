import math
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
AU = 149597870700  # Astronomical Unit in meters
COLLISION_DISTANCE = 1e9  # 1 million km collision distance

# Time step and simulation steps
dt = 86400  # Time step in seconds (1 day)
num_steps = 365  # Simulate for 1 Earth year

# Define the Sun and planets with real data
# Position data is simplified to circular orbits in the x-y plane
# Velocities are approximated based on orbital periods
planets = [
    # Sun (at the center)
    {
        'Name': 'Sun',
        'Mass': 1.989e30,
        'Position (x, y, z)': [0, 0, 0],
        'Velocity (vx, vy, vz)': [0, 0, 0]
    },
    # Mercury
    {
        'Name': 'Mercury',
        'Mass': 3.285e23,
        'Position (x, y, z)': [0.387 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 47400 * 2, 0]
    },
    # Venus
    {
        'Name': 'Venus',
        'Mass': 4.867e24,
        'Position (x, y, z)': [0.723 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 35000 * 2, 0]
    },
    # Earth
    {
        'Name': 'Earth',
        'Mass': 5.972e24,
        'Position (x, y, z)': [1.0 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 29800 * 2, 0]
    },
    # Mars
    {
        'Name': 'Mars',
        'Mass': 6.39e23,
        'Position (x, y, z)': [1.524 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 24100 * 2, 0]
    },
    # Jupiter
    {
        'Name': 'Jupiter',
        'Mass': 1.898e27,
        'Position (x, y, z)': [5.203 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 13100 * 2, 0]
    },
    # Saturn
    {
        'Name': 'Saturn',
        'Mass': 5.683e26,
        'Position (x, y, z)': [9.537 * AU * 2, 0, 0],
        'Velocity (vx, vy, vz)': [0, 9700 * 2, 0]
    }
]

# Add two asteroids with interesting orbits
Asteroids = [
    {
        'Name': 'Asteroid 1',
        'Mass': 1e15,  # Small mass compared to planets
        'Position (x, y, z)': [2.5 * AU, 0, 0.1 * AU],  # Between Mars and Jupiter
        'Velocity (vx, vy, vz)': [0, 20000, 5000]  # Some vertical motion
    },
    {
        'Name': 'Asteroid 2',
        'Mass': 1e15,
        'Position (x, y, z)': [4.0 * AU, 0, -0.1 * AU],  # In the asteroid belt
        'Velocity (vx, vy, vz)': [0, 15000, -5000]  # Opposite vertical motion
    }
]

# Combine planets and asteroids into one list
bodies = planets + Asteroids

# Store positions over time
all_positions = [[] for _ in bodies]

# Function to calculate gravitational forces
def calculate_all_gravity_forces(bodies):
    forces = [[0.0, 0.0, 0.0] for _ in bodies]

    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i != j:
                m1 = bodies[i]["Mass"]
                m2 = bodies[j]["Mass"]

                x1, y1, z1 = bodies[i]["Position (x, y, z)"]
                x2, y2, z2 = bodies[j]["Position (x, y, z)"]

                dx = x2 - x1
                dy = y2 - y1
                dz = z2 - z1

                distance = math.sqrt(dx**2 + dy**2 + dz**2)
                distance = max(distance, 1e-5)  # Avoid division by zero

                force_magnitude = (G * m1 * m2) / (distance**2)

                force_vector = [
                    force_magnitude * dx / distance,
                    force_magnitude * dy / distance,
                    force_magnitude * dz / distance
                ]

                forces[i][0] += force_vector[0]
                forces[i][1] += force_vector[1]
                forces[i][2] += force_vector[2]

    return forces

# Main simulation loop
for step in range(num_steps):
    forces = calculate_all_gravity_forces(bodies)

    # 1. Update velocities and positions
    for i in range(len(bodies)):
        vx, vy, vz = bodies[i]['Velocity (vx, vy, vz)']
        fx, fy, fz = forces[i]

        mass = bodies[i]['Mass']

        # Update velocity
        bodies[i]['Velocity (vx, vy, vz)'][0] += (fx / mass) * dt
        bodies[i]['Velocity (vx, vy, vz)'][1] += (fy / mass) * dt
        bodies[i]['Velocity (vx, vy, vz)'][2] += (fz / mass) * dt

        # Update position
        bodies[i]['Position (x, y, z)'][0] += bodies[i]['Velocity (vx, vy, vz)'][0] * dt
        bodies[i]['Position (x, y, z)'][1] += bodies[i]['Velocity (vx, vy, vz)'][1] * dt
        bodies[i]['Position (x, y, z)'][2] += bodies[i]['Velocity (vx, vy, vz)'][2] * dt

        # Store positions
        all_positions[i].append(tuple(bodies[i]['Position (x, y, z)']))

    # 2. Collision Detection (INSIDE the simulation loop)
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            x1, y1, z1 = bodies[i]["Position (x, y, z)"]
            x2, y2, z2 = bodies[j]["Position (x, y, z)"]

            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            distance = math.sqrt(dx**2 + dy**2 + dz**2)

            if distance < COLLISION_DISTANCE:
                print(f"Collision detected between Body {i+1} and Body {j+1} at distance {distance:.2e} m")

                m1 = bodies[i]["Mass"]
                m2 = bodies[j]["Mass"]

                v1 = bodies[i]['Velocity (vx, vy, vz)']
                v2 = bodies[j]['Velocity (vx, vy, vz)']

                # Elastic collision velocity updates
                new_v1 = [
                    ((m1 - m2) / (m1 + m2)) * v1[0] + ((2 * m2) / (m1 + m2)) * v2[0],
                    ((m1 - m2) / (m1 + m2)) * v1[1] + ((2 * m2) / (m1 + m2)) * v2[1],
                    ((m1 - m2) / (m1 + m2)) * v1[2] + ((2 * m2) / (m1 + m2)) * v2[2],
                ]

                new_v2 = [
                    ((2 * m1) / (m1 + m2)) * v1[0] + ((m2 - m1) / (m1 + m2)) * v2[0],
                    ((2 * m1) / (m1 + m2)) * v1[1] + ((m2 - m1) / (m1 + m2)) * v2[1],
                    ((2 * m1) / (m1 + m2)) * v1[2] + ((m2 - m1) / (m1 + m2)) * v2[2],
                ]

                bodies[i]['Velocity (vx, vy, vz)'] = new_v1
                bodies[j]['Velocity (vx, vy, vz)'] = new_v2

# Function to retrieve positions
def get_positions():
    return all_positions

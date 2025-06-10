def calculate_gravity_force(planet_mass, asteroid_mass, planet_pos, asteroid_pos):
    dx = planet_pos[0] - asteroid_pos[0]
    dy = planet_pos[1] - asteroid_pos[1]
    dz = planet_pos[2] - asteroid_pos[2]
    
    #Calculate the magnitude of the distance
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    #Avoid division by zero
    if distance == 0:
        return[0.0, 0.0, 0.0]
    
    #Calculate the gravitational force magnitude
    force_magnitude = (G * planet_mass * asteroid_mass) / (distance**2)
    
    #Normalize the distance vector
    force_direction = [dx / distance, dy / distance, dz / distance]
    
    #Scale the direction by the force magnitude to get the force vector
    force_vector = [force_magnitude * force_direction[0], force_magnitude * force_direction[1], force_magnitude * force_direction[2]]
    
    return force_vector

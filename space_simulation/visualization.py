import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from simulation import planets, Asteroids, get_positions, num_steps, AU

def run_visualization():
    # Get positions from the simulation
    all_positions = get_positions()

    # Create figure and 3D axis
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Planet colors and sizes
    planet_colors = ['yellow', 'gray', 'orange', 'blue', 'red', 'brown', 'gold']
    planet_sizes = [20, 5, 7, 8, 6, 15, 12]  # Sizes are not to scale, just for visualization

    # Asteroid colors and sizes
    asteroid_colors = ['white', 'lightgray']
    asteroid_sizes = [3, 3]  # Smaller than planets

    # Initialize the plot elements for each body
    planet_lines = []
    planet_dots = []
    planet_labels = []
    asteroid_lines = []
    asteroid_dots = []
    asteroid_labels = []

    # Initialize the plot elements for planets
    for i in range(len(planets)):
        line, = ax.plot([], [], [], '-', alpha=0.3, color=planet_colors[i])
        dot, = ax.plot([], [], [], 'o', markersize=planet_sizes[i], color=planet_colors[i])
        label = ax.text(0, 0, 0, planets[i]['Name'], color=planet_colors[i])
        planet_lines.append(line)
        planet_dots.append(dot)
        planet_labels.append(label)

    # Initialize the plot elements for asteroids
    for i in range(len(Asteroids)):
        line, = ax.plot([], [], [], '-', alpha=0.2, color=asteroid_colors[i])
        dot, = ax.plot([], [], [], 'o', markersize=asteroid_sizes[i], color=asteroid_colors[i])
        label = ax.text(0, 0, 0, Asteroids[i]['Name'], color=asteroid_colors[i])
        asteroid_lines.append(line)
        asteroid_dots.append(dot)
        asteroid_labels.append(label)

    # Set axis limits based on Saturn's orbit (the outermost planet in our simulation)
    limit = 10 * AU
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit/4, limit/4)  # Smaller Z limit since orbits are in X-Y plane
    ax.set_xlabel('X Position (AU)')
    ax.set_ylabel('Y Position (AU)')
    ax.set_zlabel('Z Position (AU)')
    ax.set_title('Solar System Simulation')

    # Convert axis ticks to AU
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/AU:.1f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/AU:.1f}'))
    ax.zaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/AU:.1f}'))

    # Animation update function
    def update(frame):
        # Update planets
        for i in range(len(planets)):
            positions = all_positions[i][:frame+1]  # Get position history up to this frame
            x, y, z = zip(*positions)  # Unpack x, y, z coordinates
            
            # Update trail
            planet_lines[i].set_data(x, y)
            planet_lines[i].set_3d_properties(z)
            
            # Update current position
            planet_dots[i].set_data(x[-1:], y[-1:])
            planet_dots[i].set_3d_properties(z[-1:])
            
            # Update label position
            planet_labels[i].set_position((x[-1], y[-1]))
            planet_labels[i].set_3d_properties(z[-1], 'z')

        # Update asteroids
        for i in range(len(Asteroids)):
            positions = all_positions[len(planets) + i][:frame+1]
            x, y, z = zip(*positions)
            
            # Update trail
            asteroid_lines[i].set_data(x, y)
            asteroid_lines[i].set_3d_properties(z)
            
            # Update current position
            asteroid_dots[i].set_data(x[-1:], y[-1:])
            asteroid_dots[i].set_3d_properties(z[-1:])
            
            # Update label position
            asteroid_labels[i].set_position((x[-1], y[-1]))
            asteroid_labels[i].set_3d_properties(z[-1], 'z')

        return planet_lines + planet_dots + planet_labels + asteroid_lines + asteroid_dots + asteroid_labels

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=num_steps, 
                                interval=50, blit=False)

    plt.show()

if __name__ == "__main__":
    run_visualization()

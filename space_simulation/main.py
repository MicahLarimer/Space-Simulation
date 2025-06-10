"""
Space Simulation Project
A 3D simulation of the solar system with planets and asteroids.
"""

import simulation
import visualization

def main():
    """
    Main entry point for the space simulation project.
    Runs the simulation and visualization.
    """
    print("Starting Space Simulation...")
    print("Running simulation with:")
    print(f"- {len(simulation.planets)} planets")
    print(f"- {len(simulation.Asteroids)} asteroids")
    print(f"- Simulation duration: {simulation.num_steps} days")
    
    # The simulation is already run when we import simulation.py
    # Now we just need to run the visualization
    visualization.run_visualization()

if __name__ == "__main__":
    main()

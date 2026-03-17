import tkinter as tk
import numpy as np
import random

class KetupatParticleSwarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Ketupat Particle Formations")
        self.width = 800
        self.height = 800
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="#1E1E1E")
        
        # UI Header
        tk.Label(root, text="Ketupat Raye.....", 
                 font=("Helvetica", 16, "bold"), fg="white", bg="#1E1E1E").pack(pady=10)

        # Create Canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.particles = []
        self.particle_size = 3
        
        # 1. Compute target points via mathematics
        self.targets = self.calculate_target_points()
        
        # 2. Spawn particles
        self.spawn_particles()
        
        # 3. Start Animation
        self.animate()

    def calculate_target_points(self):
        print("Calculating math targets for particle swarm...")
        targets = []
        # Grid range equivalent to our math bounding box
        grid_size = 120
        x = np.linspace(-1.5, 1.5, grid_size)
        y = np.linspace(-1.5, 1.5, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Evaluate equation
        a = 0.05
        b = 8
        equation_val = np.abs(X) + np.abs(Y) + a * np.abs(np.sin(b * (X + Y))) + a * np.abs(np.sin(b * (X - Y)))
        mask = equation_val <= 1.0
        
        # Scale to canvas coordinates
        scale = 300 
        x_offset = self.width / 2
        y_offset = self.height / 2
        
        for i in range(grid_size):
            for j in range(grid_size):
                if mask[i, j]:
                    # Screen space coordinate conversion
                    target_x = x_offset + (X[i, j] * scale)
                    # Note: matrix indexing [i,j] -> Y is row (i), X is col (j)
                    target_y = y_offset + (Y[i, j] * scale) 
                    targets.append((target_x, target_y))
                    
        print(f"Calculated {len(targets)} particle target coordinate points.")
        # Shuffle targets so particles fill in randomly
        random.shuffle(targets)
        return targets

    def spawn_particles(self):
        for target in self.targets:
            # Origin is randomized around the edges of the screen
            if random.choice([True, False]):
                # Spawn top/bottom
                start_x = random.randint(0, self.width)
                start_y = random.choice([-50, self.height + 50])
            else:
                # Spawn left/right
                start_x = random.choice([-50, self.width + 50])
                start_y = random.randint(0, self.height)
            
            # Draw particle on canvas
            color = random.choice(['#228B22', '#006400', '#32CD32']) # Forest, Dark, Lime green
            item_id = self.canvas.create_rectangle(
                start_x, start_y, 
                start_x + self.particle_size, start_y + self.particle_size, 
                fill=color, outline=""
            )
            
            # Store particle state
            # x, y, tx, ty, id, speed_multiplier (individual variance)
            speed = random.uniform(0.02, 0.08)
            self.particles.append([start_x, start_y, target[0], target[1], item_id, speed])

    def animate(self):
        # Update particles towards their target
        all_arrived = True
        
        for p in self.particles:
            cx, cy, tx, ty, item_id, speed = p
            
            # Calculate distance
            dx = tx - cx
            dy = ty - cy
            
            # Simple easing towards target
            if abs(dx) > 0.5 or abs(dy) > 0.5:
                all_arrived = False
                move_x = dx * speed
                move_y = dy * speed
                
                # Update current pos internal state
                p[0] += move_x
                p[1] += move_y
                
                # Update canvas graphics
                self.canvas.move(item_id, move_x, move_y)

        if not all_arrived:
            # 60 FPS update
            self.root.after(16, self.animate)
        else:
            print("Swarm assembly complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KetupatParticleSwarmApp(root)
    root.mainloop()

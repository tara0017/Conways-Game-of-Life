# Conways-Game-of-Life
Explore multiple variations of Conway's Game of Life



Inspiration:

	This project is inspired by Conway’s Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), 
	I’d like to create an interactive visual display and expand it to to include additional 2D and 3D surface.


Goal:

	Different 2D surfaces:
		Regular tessellations 
		Tessellations consisting of a mix of regular polygons 
		Tessellations of irregular polygons (M.C. Escher drawings https://mcescher.com/)

	Different 3D surfaces:
		Regular polyhedrons 
		Irregular polyhedrons

	Game variations:
		Allow user to select their own rules for survival and birth
		Allow for a cell to have a non-binary state (dead or alive), but also increased “strength”

Questions to explore:

	What do “still-life" objects look like in each surface?
	What do “oscillator” objects look like in each surface?
	What do “spaceship” objects look like in each surface?
	For the 3D surfaces is it possible to create a “snake” that wraps around to consume itself?


To do list:

	VERSION #1
	create basic GUI for square tiling
		User selects starting pattern
		Rules are preset to basic rules B3S23 (a cell is born if it has exactly 3 neighbors, and a cell  survives if it has 2 or 3 neighbors)
			* next version user will be able to set their own rules
	
	VERSION #2
	Add the other 2 regular tessellations (triangle and hexagon)


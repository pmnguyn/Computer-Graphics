# Description
For this project, I will implement a set of function in python to create a simple animated scene.
The scene is motionless and has no perspective:

![Figure_1](https://user-images.githubusercontent.com/84541835/160904372-07ff4ded-ae50-4fd7-ac79-1678fa297713.png)

After being implemented, the house rotates around the y-axis. Each step of the animation will be called with 
i equal to the step number. It should achieve one full rotation during the 150 steps of the animation.
On step 150, it should be back to where it started.

https://user-images.githubusercontent.com/84541835/160910372-04f41449-0384-4256-81b0-911ebc906fc1.mov

Next, make the ball move a total of 20 units to the right when seen from the front. At the end of the 150
steps, it should have moved the full distance; in between, it should move in equal steps. 


https://user-images.githubusercontent.com/84541835/160911194-d97ac4af-3416-4a6d-82ba-e334c7221c3b.mov

Finally, I will make the ball roll around its center naturally. For each rotation, I will translate 
the ball to the origin, apply the rotation, and then translate the ball to its proper location. 
The ball should make one full rotation over the 150 steps. At the end of the 150 steps, it should be in the same
orientation as it started. 


https://user-images.githubusercontent.com/84541835/160912435-84fdae73-34b0-4182-9ad7-56ce3b2770a3.mov


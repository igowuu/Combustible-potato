# The Combustible Potato (FRC 5113)

Team 5113's 2026 FRC robot code for practice, officially known as The Combustible Potato. The potato's code is written in Python and is based on Robotpy's TimedRobot control system.

The code is divided into several packages and files, each responsible for a different aspect of the robot function. This README explains the function of each package, and some of the variable naming conventions used. Additional information about each specific class can be found in that class's Python file.

## File Structure
Our file structure is designed for simplicity, maintainability, and ease of expansion throughout the season.

[`robot.py`](src/robot.py)

Initializes all components of the program and orchestrates the overall program flow.
We use TimedRobot, a simple wpilib framework that allows us to subclass it to create our main robot logic.

[`physics.py`](src/physics.py)

Initializes all simulated components of the program and orchestrates the additional simulation logic.
Simulation is closely tied with existing files, so changes to all other files will likely be put into effect here.

[`controls`](src/controls)

Defines high-level robot behaviors and decision-making logic.  
Determines when and how component actions are triggered, often based on inputs or robot state.

[`components`](src/components)

Initializes and manages low-level hardware interfaces such as motors, sensors, and encoders.  
Provides clean, reusable methods for reading hardware state and issuing control commands.

[`constants`](src/constants)

Stores hardware-specific values such as max voltages and deadbands.  
Centralizes configuration to ensure consistency and simplify updates across the codebase.

[`utils`](src/utils)

Contains general-purpose helper functions and shared utilities.  
Provides reusable logic that does not belong to a specific robot subsystem.

[`tests`](src/tests)

Includes unit tests and built-in checks for validating robot code behavior.  
Helps ensure reliability, correctness, and safe operation during development.


## Requirements
requirements.txt is included for all packages.

## Test Code

```
robotpy test
```

## Run Simulation

```
robotpy sim
```

## Deploy to Robot

```
robotpy deploy
```

# Legend of the Potato
*<pre>
Born of sparks and deadly flame,
The Combustible Potato rose to fame;
With yummy circuits and gears aglow,
a legend destined to burn and grow.
</pre>*

# Variational Quantum Monte Carlo

## Code review notes

Please read the "About the Code" section. Please note, that tere are currently small bugs present, that prevent you from running the code. If you have any suggestions, how to avoid the MCIntegrator-for-loops, please let us know!



## Project Problem description

Reader for the Monte-Carlo-Method: https://gitlab.kwant-project.org/computational_physics_17/course_notes/blob/master/project%202/montecarlo_intro.pdf


Reader for the Variational Quantum Monte Carlo: https://gitlab.kwant-project.org/computational_physics_17/course_notes/blob/master/project%202/projects.md


Part of the book for the Variational Quantum Monte Carlo: https://gitlab.kwant-project.org/computational_physics_17/course_notes/blob/master/project%202/background_reading/TheMonteCarloMethod.pdf


PDF of book of Application of Quantum Mechanics: https://gitlab.kwant-project.org/computational_physics_17/course_notes/blob/master/project%202/background_reading/aqm.pdf 



## About the Code

The code is structured into three main parts:

1  MCIntegrator.py
2  VariationalQuantumSimulator.py
3  Harmonic.py / Hydrogen.py / Helium.py / etc

The first of these three does the integration with the option of diffent integration point modes. The second file defines a gerneral Monte-Carlo Variational Quantum Simulation. Finally files can be written, that define the test function etc, that run the aforementioned simulation for a specific system.

The file IntegralTest.py was used for benchmarking the different integration methods. The file BoxPlotter.py can be used to plot the integration points. temp.py is just for testing code.

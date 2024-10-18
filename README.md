**Project Summary:** Developed a program that optimizes delivery routes for trucks, ensuring timely package delivery while minimizing fuel consumption.

**Implementation Steps:** This project provided a list of addresses, distances between said addresses, and a set of packages. I had to parse the data and develop a program that efficiently delivered the packages, ensuring timely deliveries while keeping the trucks within a specified fuel limit.

The first step was to create a hashmap that stores all package data, allowing for easy insertion and removal. Each package received a unique ID, and important information was stored, including the delivery address, weight, and deadline.

Next, I developed an adjacency matrix to calculate the distances between delivery addresses. The program parses the given file to create this matrix. I implemented Dijkstra's algorithm to determine the best routes for the trucks, running the algorithm before each departure. I chose this algorithm for its efficiency, as a depth-first search would impose too much load on the computer if the project scaled.

Additionally, the project includes a feature to track package delivery times. By entering a specific time, users can view the status of all trucks. It also allows users to access package information by package ID.

Ultimately, all packages were delivered on time, and the trucks remained within the fuel limit.

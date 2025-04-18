import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(0)

# Function to generate a random number in the interval [a, b)
def random(a, b):
    return a + (b - a) * np.random.random()

probs = np.arange(40, 80, 5) #fit every bet into its respective Probability group
overs = np.arange(0, 40, 5) #fit every bet into its respective Probability group
print(overs)

# Given data points
y = [1.000000, 0.731689, 0.070737, -0.628174, -0.989992, -0.820559, -0.210796, 0.512085, 0.960170]
z = [0.00000, 0.68164, 0.99749, 0.77807, 0.14112, -0.57156, -0.97753, -0.85893, -0.27942]

len_y = len(y)

# Generate xEnd values to represent the intervals [0, 2]
xEnd = np.linspace(0, 2, len_y)

# Find the minimum and maximum values among y and z
minFG = min(min(y), min(z))
maxFG = max(max(y), max(z))

# Number of random points to generate
n = 2000

# Function for linear interpolation (used in Monte Carlo method)
def S(x, x_1, y_1, x_2, y_2):
    return y_1 + ((y_2 - y_1) / (x_2 - x_1)) * (x - x_1)

tot = cntIn = 0  # Initialize counters for total points and points inside the region of interest

# Monte Carlo method for numerical integration
for p_iter in range(2000):
    # Generate a random point (p_x, p_y)
    p_x, p_y = random(0, 2), random(minFG, maxFG)

    # Find the interval for the random point
    idx = len_y - 2 # if nothing holds set that the point belongs to the last interval
    for j in range(1, len_y - 1):
        if xEnd[j - 1] < p_x < xEnd[j]:
            idx = j - 1
            break

    # Perform linear interpolation to get spline values at p_x
    spline_y = S(p_x, xEnd[idx], y[idx], xEnd[idx + 1], y[idx + 1])
    spline_z = S(p_x, xEnd[idx], z[idx], xEnd[idx + 1], z[idx + 1])

    tot += 1  # Increment total points

    # Check if the random point is inside the region defined by the splines
    if min(spline_y, spline_z) < p_y < max(spline_y, spline_z):
        plt.plot(p_x, p_y, 'r+')  # Plot in red if inside
        cntIn += 1  # Increment points inside counter
    else:
        plt.plot(p_x, p_y, 'g+')  # Plot in green if outside

# Estimate the integral using the Monte Carlo method
integral = ((xEnd[len_y - 1] - xEnd[0]) * (maxFG - minFG)) * (cntIn / tot)

# Print the estimated integral
print('Integral :=', integral)

# Plot the points and the result
plt.title('Integral %s' % (integral))
plt.show()

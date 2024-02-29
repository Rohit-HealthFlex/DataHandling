import math
import time

def smoothing_factor(t_e, cutoff):
    r = 2 * math.pi * cutoff * t_e
    return r / (r + 1)

def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev

class OneEuroFilter:
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        """Initialize the one euro filter."""
        # The parameters.
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        # Previous values.
        self.x_prev = float(x0)
        self.dx_prev = float(dx0)
        self.t_prev = float(t0)

    def __call__(self, t, x):
        """Compute the filtered signal."""
        t_e = t - self.t_prev

         # Check if time difference is close to zero
        if abs(t_e) < 1e-6:
        # Return the current value without filtering
          return x

        # The filtered derivative of the signal.
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = exponential_smoothing(a_d, dx, self.dx_prev)

        # The filtered signal.
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = smoothing_factor(t_e, cutoff)
        x_hat = exponential_smoothing(a, x, self.x_prev)

        # Memorize the previous values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat

# Given array of accelerations
accelerations = [0.9, 0.8, 0.1, 1.0, 13.0, 13.0]

# Initialize OneEuroFilter\
'''min_cutoff is usually relatively small to allow the filter to adapt to slow variations in the 
input signal while attenuating high-frequency noise. Common values may range from 0.1 to positive integers'''

'''A smaller d_cutoff allows the filter to adapt more quickly to changes in the derivative, 
while a larger d_cutoff results in slower adaptation.
If signal derivative varies rapidly, smaller d_cutoff to capture changes, while slower variations may require a larger d_cutoff.
Similar Range to min_cutoff - from 0.1 Hz to postive integers
'''
# Lower beta value provides more aggressive filteration, range is between 0 to 1

one_euro_filter = OneEuroFilter(t0=0, x0=accelerations[0], min_cutoff= 0.1, beta=0.1, d_cutoff= 0.001)

#start_time_1euro = time.time()
# Apply the filter to each acceleration value
filtered_accelerations_1euro = []
for i, acceleration in enumerate(accelerations):
    filtered_acceleration = one_euro_filter(i, acceleration)
    filtered_accelerations_1euro.append(filtered_acceleration)

#end_time_1euro = time.time()

#inference_time_1euro = end_time_1euro - start_time_1euro

# Print the filtered accelerations
print("Original Accelerations:", accelerations)
print("Filtered Accelerations:", filtered_accelerations_1euro)
from collections import deque

class Smoother:
    def __init__(self, short_window_size, long_window_size, alpha, beta):
        self.short_window = deque(maxlen=short_window_size)
        self.long_window = deque(maxlen=long_window_size)
        self.alpha = alpha
        self.beta = beta

    def add_data_point(self, data_point):
        self.short_window.append(data_point)
        self.long_window.append(data_point)

    def smooth_value(self):
        if len(self.long_window) < self.long_window.maxlen:
            return None  # Not enough data points yet

        short_window_sum = sum(self.short_window)
        long_window_sum = sum(self.long_window)

        short_window_average = short_window_sum / len(self.short_window)
        long_window_average = long_window_sum / len(self.long_window)

        smoothed_value = self.alpha * short_window_average + self.beta * long_window_average

        return smoothed_value

# Example usage:
if __name__ == "__main__":
    # Initialize smoother object
    smoother = Smoother(short_window_size=3, long_window_size=7, alpha=0.2, beta=0.8)

    # Add some data points
    data_points = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 7, 8, 9, 20]  # 11 ones in the beginning
    for data_point in data_points:
        smoother.add_data_point(data_point)

    # Smooth the values
    smoothed_value = smoother.smooth_value()
    print("Smoothed Value:", smoothed_value)
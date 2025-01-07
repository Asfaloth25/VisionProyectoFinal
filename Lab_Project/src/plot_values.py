import cv2
import numpy as np
import matplotlib.pyplot as plt


def update_real_time_graph(data, ax, line):
    """
    Updates the Matplotlib graph with new data in real time.
    
    :param data: List of data points to plot.
    :param ax: The Matplotlib Axes object for the graph.
    :param line: The line object to update with new data.
    """
    line.set_ydata(data)
    line.set_xdata(range(len(data)))
    ax.relim()  # Recompute the limits based on new data
    ax.autoscale_view()  # Rescale the view to fit the data
    plt.pause(0.001)  # Pause for the plot to update


# Real-time simulation with OpenCV and Matplotlib
if __name__ == "__main__":
    # Create a dummy OpenCV image
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    # Initialize Matplotlib
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    ax.set_title("Real-Time Graph")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    line, = ax.plot([], [], 'g-', label="Data")
    ax.legend()

    # Data buffer for the graph
    graph_data = [0] * 100  # Start with 100 points

    # Real-time loop
    while True:
        # Simulate data updates
        new_value = np.random.randint(10, 50)
        graph_data.append(new_value)
        graph_data = graph_data[-100:]  # Keep only the last 100 points

        # Update the Matplotlib graph
        update_real_time_graph(graph_data, ax, line)

        # Update the OpenCV image
        cv2.putText(img, f"Latest Value: {new_value}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Real-Time Image", img)

        # Break loop on 'Esc' key
        if cv2.waitKey(30) & 0xFF == 27:
            break

    # Cleanup
    cv2.destroyAllWindows()
    plt.ioff()
    plt.show()

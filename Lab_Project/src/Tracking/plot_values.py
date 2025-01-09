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
    ax.relim()
    ax.autoscale_view()
    plt.pause(0.001)  # Pause for the plot to update



if __name__ == "__main__":
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    ax.set_title("Real-Time Graph")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    line, = ax.plot([], [], 'g-', label="Data")
    ax.legend()

    graph_data = [0] * 100  # Start with 100 points

    while True:
        new_value = np.random.randint(10, 50)
        graph_data.append(new_value)
        graph_data = graph_data[-100:]

        update_real_time_graph(graph_data, ax, line)

        cv2.putText(img, f"Latest Value: {new_value}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Real-Time Image", img)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    # Cleanup
    cv2.destroyAllWindows()
    plt.ioff()
    plt.show()

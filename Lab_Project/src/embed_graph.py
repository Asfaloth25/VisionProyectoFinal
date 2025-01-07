import cv2
import numpy as np


def embed_graph_on_image(image: np.ndarray, data: list, 
                        position: tuple = (0, 0), size: tuple = (200, 200)) -> np.ndarray:
    """
    Draw a graph directly on an OpenCV image in real-time.
    
    :param image: Input OpenCV image (numpy array).
    :param data: List of data points to plot.
    :param position: Top-left position to place the graph.
    :param size: Size of the graph (width, height).
    :return: OpenCV image with the graph embedded.
    """
    # Parameters for the graph area
    graph_width, graph_height = size
    x, y = position

    # Create a blank canvas for the graph
    graph_img = np.zeros((graph_height, graph_width, 3), dtype=np.uint8)

    # Normalize data to fit within the graph height
    data = np.array(data, dtype=np.float32)
    if len(data) > graph_width:  # Downsample if data exceeds graph width
        data = cv2.resize(data.reshape(1, -1), (graph_width, 1), interpolation=cv2.INTER_LINEAR).flatten()
    normalized_data = cv2.normalize(data, None, 0, graph_height - 1, cv2.NORM_MINMAX)

    # Draw the graph as a polyline
    for i in range(1, len(normalized_data)):
        start_point = (i - 1, graph_height - int(normalized_data[i - 1]))
        end_point = (i, graph_height - int(normalized_data[i]))
        cv2.line(graph_img, start_point, end_point, (0, 255, 0), 1)

    # Overlay the graph onto the original image
    overlay = image.copy()
    overlay[y:y+graph_height, x:x+graph_width] = graph_img

    return overlay


# Example Usage
if __name__ == "__main__":
    # Create a dummy OpenCV image
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    # Real-time simulation
    graph_data = [10, 20, 15, 30, 25, 35, 40]  # Example data
    while True:
        # Simulate data updates
        graph_data.append(np.random.randint(10, 50))
        graph_data = graph_data[-100:]  # Keep the last 100 points

        # Draw graph on the image
        img_with_graph = draw_graph_directly(img, graph_data, position=(10, 10), size=(150, 150))

        # Display the result
        cv2.imshow("Real-Time Graph", img_with_graph)
        if cv2.waitKey(30) & 0xFF == 27:  # Exit on 'Esc' key
            break

    cv2.destroyAllWindows()

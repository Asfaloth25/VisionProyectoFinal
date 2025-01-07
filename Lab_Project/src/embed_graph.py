import cv2
import numpy as np
from matplotlib import pyplot as plt


def embed_graph_on_image(image: np.ndarray, data: list, 
                         position: tuple = (0, 0), size: tuple = (200, 200)) -> np.ndarray:
    """
    Embed a matplotlib graph in the top-left corner or any specified position of a cv2 image.

    :param image: Input OpenCV image (numpy array)
    :param data: List of data points to plot.
    :param position: Position to place the graph (top-left corner by default).
    :param size: Size of the graph (width, height).
    :return: OpenCV image with embedded graph.
    """
    # Create the plot with matplotlib
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set_title("Graph")
    ax.grid(True)

    # Remove axes and whitespace around the plot
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Convert the plot to a numpy array (image)
    fig.canvas.draw()
    graph_width, graph_height = fig.canvas.get_width_height()
    graph_img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    graph_img = graph_img.reshape((graph_height, graph_width, 3))

    # Resize the graph image to fit into the specified size
    graph_img = cv2.resize(graph_img, size)

    # Convert RGB to BGR for OpenCV compatibility
    graph_img = cv2.cvtColor(graph_img, cv2.COLOR_RGB2BGR)

    # Embed the graph in the original image
    x, y = position
    overlay = image.copy()
    overlay[y:y+size[1], x:x+size[0]] = graph_img

    # Ensure the graph fits in the image boundaries
    if y + size[1] > image.shape[0] or x + size[0] > image.shape[1]:
        raise ValueError("Graph size and position exceed image dimensions.")

    return overlay


# Example usage:
if __name__ == "__main__":
    # Create a dummy OpenCV image
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    # Sample data for the graph
    sample_data = [10, 20, 15, 30, 25, 35, 40]

    # Add the graph to the image
    img_with_graph = embed_graph_on_image(img, sample_data, position=(10, 10), size=(150, 150))

    # Show the result
    cv2.imshow("Image with Graph", img_with_graph)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

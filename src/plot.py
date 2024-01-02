import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

def normalize_2d_vector(x, y):
    magnitude = math.sqrt(x ** 2 + y ** 2)  # Calculate the magnitude of the vector

    # Normalize the vector
    normalized_x = x / magnitude if magnitude != 0 else 0
    normalized_y = y / magnitude if magnitude != 0 else 0

    return normalized_x, normalized_y

def extract_unique_points(routes):
    unique_points = []
    seen = set()

    for route in routes:
        for point in route:
            if point not in seen:
                unique_points.append(point)
                seen.add(point)

    return unique_points


def plot_routes(routes):

    # list every unique point
    points = extract_unique_points(routes)
    print(points)

    # calculate each route count
    route_counts = {}
    for route in routes:
        if route in route_counts:
            route_counts[route] += 1
        else:
            route_counts[route] = 1

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Map variables:
    point_size = 10
    arrow_tip_size = 20
    arrow_curve_factor = 0.1
    arrow_shortening_factor = 0.09  # arrows should be shorter to not overlap the radius of points
    count_text_displacement_factor = 0.09  # how much further the text is from the middle of the arrow to the right (perpendicually)
    end_arrow_tip_displacement = 0.02  # slightly shift the end tip to avoid arrows overlapping

    angles = np.linspace(0, 2 * np.pi, len(points), endpoint=False)
    circle_x = np.cos(angles)
    circle_y = np.sin(angles)

    # Dictionary to store coordinates of each point
    point_coordinates = {point: (x, y) for point, x, y in zip(points, circle_x, circle_y)}

    # print(point_coordinates)

    # Draw points
    for point, (x, y) in point_coordinates.items():
        ax.plot(x, y, 'o', markersize=point_size, label=point)
        ax.text(x, y+0.06, point, ha='center', va='center')

    # Calculate routes
    for route, count in route_counts.items():

        first_point, second_point = route
        start_x, start_y = point_coordinates[first_point]
        end_x, end_y = point_coordinates[second_point]

        # Displacement vectors:
        displacement_vector_x = end_x - start_x
        displacement_vector_y = end_y - start_y

        # Normalized vectors:
        normalized_vector_x, normalized_vector_y = normalize_2d_vector(displacement_vector_x, displacement_vector_y)

        # Calculate arrows adjustments for start and end points:
        a_start_x = start_x + normalized_vector_x * arrow_shortening_factor
        a_start_y = start_y + normalized_vector_y * arrow_shortening_factor
        # the direction coordinates are turned 90 degrees to shift the end tip to the right.
        a_end_x = end_x - normalized_vector_x * arrow_shortening_factor + end_arrow_tip_displacement * normalized_vector_y
        a_end_y = end_y - normalized_vector_y * arrow_shortening_factor + end_arrow_tip_displacement * -normalized_vector_x

        # Calculate the plot of a curved arrow between points
        arrow = FancyArrowPatch(
            (a_start_x, a_start_y),                              # start point
            (a_end_x, a_end_y),                                  # end point
            connectionstyle=f"arc3,rad={arrow_curve_factor}",         # curved factor
            arrowstyle="->",                                          # style
            mutation_scale=arrow_tip_size,                            # arrow size
            linewidth=1 + math.log(count)                             # arrow width based on count in logarithmic scale
        )

        ax.add_patch(arrow)

        # Calculate the point to place the text
        arrow_mid_x = start_x + displacement_vector_x / 2
        arrow_mid_y = start_y + displacement_vector_y / 2

        text_x = arrow_mid_x + count_text_displacement_factor * displacement_vector_y
        text_y = arrow_mid_y + count_text_displacement_factor * -displacement_vector_x

        # write route count above the route
        ax.text(text_x, text_y, str(count), ha='center', va='center', fontsize = 10 + math.log(count), weight = 1000)

    plt.axis("off")
    # plt.show()
    plt.savefig('graph.png')


sample_routes = [
        ("sensor1", "sensor2"),
        ("sensor2", "sensor1"),
        ("sensor1", "sensor6"),
        ("sensor1", "sensor6"),
        ("sensor6", "sensor5"),
        ("sensor5", "sensor6"),
        ("sensor6", "sensor5"),
        ("sensor5", "sensor2"),
        ("sensor5", "sensor3"),
        ("sensor5", "sensor4"),
        ("sensor5", "sensor4"),
        ("sensor4", "sensor3"),
        ("sensor3", "sensor2"),
        ("sensor3", "sensor2"),
        ("sensor3", "sensor2")
    ]

new_routes = [
        ("raspPI1", "raspPI2"),
        ("raspPI2", "raspPI1"),
        ("raspPI1", "raspPI3"),
        ("raspPI3", "raspPI2"),
        ("raspPI2", "raspPI1")
]

plot_routes(sample_routes)



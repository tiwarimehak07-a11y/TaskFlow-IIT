from backend.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


# Synthetic task data (same fields as our app uses)
def generate_tasks(size):

    tasks = []

    for i in range(size):

        tasks.append(
            {
                "id": i,
                "title": f"Task {i}",
                "priority": (
                    "high"
                    if i % 3 == 0
                    else "medium"
                    if i % 3 == 1
                    else "low"
                ),
                "due_date": "2026-08-10"
            }
        )

    return tasks



sizes = [10, 500, 3000]


for size in sizes:

    print("\n----------------------")
    print("DATA SIZE:", size)
    print("----------------------")


    tasks = generate_tasks(size)


    # Insertion Sort Benchmark

    sort_data = tasks.copy()

    insertion_count = insertion_sort_count(
        sort_data,
        "title"
    )


    print(
        "Insertion Sort Comparisons:",
        insertion_count
    )


    # Binary Search Benchmark
    # Need sorted data first

    binary_data = tasks.copy()

    insertion_sort_count(
        binary_data,
        "title"
    )


    binary_result = binary_search_count(
        binary_data,
        "Task 250",
        "title"
    )


    print(
        "Binary Search:",
        binary_result
    )


    # Linear Search Benchmark

    linear_result = linear_search_count(
        tasks,
        "Task 250",
        "title"
    )


    print(
        "Linear Search:",
        linear_result
    )
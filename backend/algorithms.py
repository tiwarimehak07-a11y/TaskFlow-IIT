def priority_value(priority: str):
    priority = priority.lower()

    if priority == "high":
        return 3

    elif priority == "medium":
        return 2

    return 1


def insertion_sort(tasks):

    for i in range(1, len(tasks)):

        current = tasks[i]

        j = i - 1

        while (
            j >= 0
            and priority_value(tasks[j].priority)
            < priority_value(current.priority)
        ):

            tasks[j + 1] = tasks[j]

            j -= 1

        tasks[j + 1] = current

    return tasks
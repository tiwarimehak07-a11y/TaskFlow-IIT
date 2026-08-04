def priority_value(priority: str):
    priority = priority.lower()

    if priority == "low":
        return 1
    elif priority == "medium":
        return 2
    elif priority == "high":
        return 3

    return 0


# -------------------------
# INSERTION SORT
# -------------------------

def insertion_sort(records, key):

    for i in range(1, len(records)):

        current = records[i]

        j = i - 1

        while (
            j >= 0
            and records[j][key] > current[key]
        ):

            records[j + 1] = records[j]

            j -= 1

        records[j + 1] = current


# -------------------------
# BINARY SEARCH
# -------------------------

def binary_search(sorted_records, target_value, key):

    low = 0
    high = len(sorted_records) - 1

    while low <= high:

        mid = (low + high) // 2

        if sorted_records[mid][key] == target_value:
            return mid

        elif sorted_records[mid][key] < target_value:
            low = mid + 1

        else:
            high = mid - 1

    return -1


# -------------------------
# LINEAR SEARCH
# -------------------------

def linear_search(records, target_value, key):

    for i in range(len(records)):

        if records[i][key] == target_value:
            return i

    return -1


# -------------------------
# INSERTION SORT COUNT
# -------------------------

def insertion_sort_count(records, key):

    comparisons = 0

    for i in range(1, len(records)):

        current = records[i]

        j = i - 1

        while j >= 0:

            comparisons += 1

            if records[j][key] > current[key]:

                records[j + 1] = records[j]

                j -= 1

            else:
                break

        records[j + 1] = current

    return comparisons


# -------------------------
# BINARY SEARCH COUNT
# -------------------------

def binary_search_count(sorted_records, target_value, key):

    comparisons = 0

    low = 0
    high = len(sorted_records) - 1

    while low <= high:

        comparisons += 1

        mid = (low + high) // 2

        if sorted_records[mid][key] == target_value:

            return {
                "index": mid,
                "comparison_count": comparisons
            }

        elif sorted_records[mid][key] < target_value:

            low = mid + 1

        else:

            high = mid - 1

    return {
        "index": -1,
        "comparison_count": comparisons
    }


# -------------------------
# LINEAR SEARCH COUNT
# -------------------------

def linear_search_count(records, target_value, key):

    comparisons = 0

    for i in range(len(records)):

        comparisons += 1

        if records[i][key] == target_value:

            return {
                "index": i,
                "comparison_count": comparisons
            }

    return {
        "index": -1,
        "comparison_count": comparisons
    }
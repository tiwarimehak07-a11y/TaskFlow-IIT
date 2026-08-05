def parse_task(description: str):

    text = description.lower()

    # Priority
    if "urgent" in text or "asap" in text:
        priority = "high"

    elif "whenever" in text or "low priority" in text:
        priority = "low"

    else:
        priority = "medium"

    # Due date
    due_date = None

    if "today" in text:
        due_date = "today"

    elif "tomorrow" in text:
        due_date = "tomorrow"

    # Title
    title = description

    words = [
        "urgent",
        "asap",
        "today",
        "tomorrow",
        "whenever",
        "low priority"
    ]

    for word in words:
        title = title.replace(word, "")

    title = title.strip()

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date
    }
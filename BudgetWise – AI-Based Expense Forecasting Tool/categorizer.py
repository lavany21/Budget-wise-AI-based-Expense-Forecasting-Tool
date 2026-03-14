def categorize_transaction(description):

    if not description:
        return "Other"

    text = description.lower().strip()

    # FOOD
    food_keywords = [
        "food","restaurant","pizza","burger","coffee",
        "noodles","rice","dal","biryani","tea","snacks",
        "maggi","pasta","dosa","idli","lunch","dinner"
    ]

    # TRANSPORT
    transport_keywords = [
        "uber","ola","bus","metro","train","fuel","petrol","taxi"
    ]

    # GROCERIES
    grocery_keywords = [
        "grocery","vegetable","milk","market","supermarket"
    ]

    # SHOPPING
    shopping_keywords = [
        "amazon","flipkart","clothes","shopping","mall"
    ]

    # ENTERTAINMENT
    entertainment_keywords = [
        "movie","netflix","game","cinema"
    ]

    # HEALTH
    health_keywords = [
        "hospital","medicine","doctor","pharmacy"
    ]

    if any(word in text for word in food_keywords):
        return "Food & Dining"

    if any(word in text for word in transport_keywords):
        return "Transport"

    if any(word in text for word in grocery_keywords):
        return "Groceries"

    if any(word in text for word in shopping_keywords):
        return "Shopping"

    if any(word in text for word in entertainment_keywords):
        return "Entertainment"

    if any(word in text for word in health_keywords):
        return "Health & Medical"

    return "Other"
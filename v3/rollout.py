import hashlib


def rollout_hash(user_id: int, salt: str = "FeatureSalt", max_value: int = 100) -> int:
    """
    Generate a deterministic 'random' value between 0 and max_value (exclusive) for a user.
    
    :param user_id: The user's unique identifier.
    :param salt: A salt string to make this hash function specific to a feature or use case.
    :param max_value: The maximum value (exclusive) that can be returned by this function.
    :return: A value between 0 and max_value (exclusive).
    """

    # Convert the user_id to string and hash it using SHA-256
    hasher = hashlib.sha256()
    hasher.update(f"{user_id}{salt}".encode())
    hashed_value = int(hasher.hexdigest(), 16)  # Convert the hash from hex to int

    return hashed_value % max_value


def is_rolled_out(user_id: int, percentage: int, salt: str = "FeatureSalt") -> bool:
    """
    Determine if a feature should be rolled out to a user based on a percentage.

    :param user_id: The user's unique identifier.
    :param percentage: The percentage of users to roll the feature out to.
    :param salt: A salt string to make this decision specific to a feature or use case.
    :return: True if the feature should be rolled out, False otherwise.
    """

    value = rollout_hash(user_id, salt)
    threshold = (percentage / 100) * 100  # Calculate the threshold based on the given percentage

    return value < threshold
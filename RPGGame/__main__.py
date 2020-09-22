from typing import List


def num_list(name: str, list: List[str]):
    """Prints numerical list with one item per line.

    Args:
        name: The name of the list.
        list: The list of values.
    """
    print(f"{name}:")
    for index, value in enumerate(list):
        print(f"{index + 1}: {value.capitalize()}")


if __name__ == "__main__":
    print("Hello World")

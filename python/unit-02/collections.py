# TODO 1: Implement the `create_container` function here.
from typing import Literal

collection_type_as_a_str = Literal["list", "set", "tuple", "dict"]


def create_container(
    container_type: collection_type_as_a_str,
) -> list | set | tuple | dict:
    if container_type == "list":
        return list()
    elif container_type == "set":
        return set()
    elif container_type == "tuple":
        return tuple()
    elif container_type == "dict":
        return dict()


# TODO 2: Implement the `access_item` function here.
def access_item(item: int, container: list | set | tuple | dict):
    if isinstance(container, list):
        return container[item]
    elif isinstance(container, set):
        return item in container
    elif isinstance(container, tuple):
        return container[item]
    elif isinstance(container, dict):
        return container[item]


# TODO 3: Implement the `add_item` function here.
def add_item(item, container: list | set | tuple | dict, position: int = None):
    if isinstance(container, list):
        if position != None:
            container.insert(position, item)
        else:
            container.append(item)
    elif isinstance(container, set):
        container.add(item)
    elif isinstance(container, tuple):
        container = list(container)
        if position != None:
            container.insert(position, item)
        else:
            container.append(item)
        container = tuple(container)
    elif isinstance(container, dict):
        if isinstance(item, tuple):
            container[item[0]] = item[1]
        else:
            container[item] = None
    return container

    # TODO 4: Implement the `remove_item` function here.


def remove_item_from_list(
    item, container: list | set | tuple, multi: bool = True
) -> list:
    if not (isinstance(container, list)):
        container = list(container)
    if multi:
        for i in container:
            if item in container:
                container.remove(item)
    else:
        container.remove(item)
    return container


def remove_item(item, container: list | set | tuple | dict, multi: bool = True):
    if isinstance(container, list):
        container = remove_item_from_list(item, container, multi)
    elif isinstance(container, set):
        container = set(remove_item_from_list(item, container, multi))
    elif isinstance(container, tuple):
        container = tuple(remove_item_from_list(item, container, multi))
    elif isinstance(container, dict):
        container.pop(item)
    return container

    # TODO 5: Implement the `update_item` function here.


def update_item_in_list(
    orig_item, new_item, container: list | set | tuple, multi: bool = True
) -> list:
    if not (isinstance(container, list)):
        container = list(container)
    for i in container:
        if i == orig_item:
            container[container.index(orig_item)] = new_item
            if not multi:
                break
    return container


def update_item(
    orig_item, new_item, container: list | set | tuple | dict, multi: bool = True
):
    if isinstance(container, list):
        container = update_item_in_list(orig_item, new_item, container, multi)
    elif isinstance(container, set):
        container = set(update_item_in_list(orig_item, new_item, container, multi))
    elif isinstance(container, tuple):
        container = tuple(update_item_in_list(orig_item, new_item, container, multi))
    elif isinstance(container, dict):
        if isinstance(new_item, tuple):
            del container[orig_item]
            container[new_item[0]] = new_item[1]
        else:
            container[orig_item] = new_item
    return container


# TODO 6: Implement the `convert_container` function here.
from typing import Literal

collection_type_as_a_str = Literal["list", "set", "tuple", "dict"]


def convert_to_list(container: list | set | tuple | dict) -> list:
    if isinstance(container, list):
        return container
    else:
        new_container = list()
        if isinstance(container, set) or isinstance(container, tuple):
            for i in container:
                new_container.append(i)
        elif isinstance(container, dict):
            for key, value in container.items():
                new_container.append((key, value))
        return new_container


def convert_to_set(container: list | set | tuple | dict) -> set:
    if isinstance(container, set):
        return container
    else:
        if isinstance(container, list) or isinstance(container, tuple):
            return set(container)
        else:
            new_container = set()
            if isinstance(container, dict):
                for key, value in container.items():
                    new_container.add((key, value))
            return new_container


def convert_to_tuple(container: list | set | tuple | dict) -> tuple:
    if isinstance(container, tuple):
        return container
    else:
        if isinstance(container, list) or isinstance(container, set):
            return tuple(container)
        else:
            new_container = list()
            if isinstance(container, dict):
                for key, value in container.items():
                    new_container.append((key, value))
            return tuple(new_container)


def convert_to_dict(container: list | set | tuple | dict) -> dict:
    if isinstance(container, dict):
        return container
    else:
        new_container = dict()
        if (
            isinstance(container, list)
            or isinstance(container, set)
            or isinstance(container, tuple)
        ):
            for i in set(container):
                if isinstance(i, tuple):
                    new_container[i[0]] = i[1]
                else:
                    new_container[i] = None
        return new_container


def convert_container(
    container: list | set | tuple | dict, container_type: collection_type_as_a_str
):
    if container_type == "list":
        return convert_to_list(container)
    elif container_type == "set":
        return convert_to_set(container)
    elif container_type == "tuple":
        return convert_to_tuple(container)
    elif container_type == "dict":
        return convert_to_dict(container)


# convert a list to a set, tuple, and dict,
assert convert_container([1, 2, 3, 4], "set") == {1, 2, 3, 4}
assert convert_container([1, 2, 3, 4], "tuple") == (1, 2, 3, 4)
assert convert_container([1, 2, 3, 4], "dict") == {1: None, 2: None, 3: None, 4: None}
assert convert_container([1, (2, "a"), 3, (4, "b")], "dict") == {
    1: None,
    2: "a",
    3: None,
    4: "b",
}

# convert a set to a list, tuple, and dict
assert convert_container({1, 2, 3, 4}, "list") == [1, 2, 3, 4]
assert convert_container({1, 2, 3, 4}, "tuple") == (1, 2, 3, 4)
assert convert_container({1, 2, 3, 4}, "dict") == {1: None, 2: None, 3: None, 4: None}
assert convert_container({1, (2, "a"), 3, (4, "b")}, "dict") == {
    1: None,
    2: "a",
    3: None,
    4: "b",
}

# convert a tuple to a list, set, and dict
assert convert_container((1, 2, 3, 4), "list") == [1, 2, 3, 4]
assert convert_container((1, 2, 3, 4), "set") == {1, 2, 3, 4}
assert convert_container((1, 2, 3, 4), "dict") == {1: None, 2: None, 3: None, 4: None}
assert convert_container((1, (2, "a"), 3, (4, "b")), "dict") == {
    1: None,
    2: "a",
    3: None,
    4: "b",
}

# convert a dict to a list, set, and tuple
assert convert_container({1: "a", 2: "b", 3: "c", 4: "d"}, "list") == [
    (1, "a"),
    (2, "b"),
    (3, "c"),
    (4, "d"),
]
assert convert_container({1: "a", 2: "b", 3: "c", 4: "d"}, "set") == {
    (1, "a"),
    (2, "b"),
    (3, "c"),
    (4, "d"),
}
assert convert_container({1: "a", 2: "b", 3: "c", 4: "d"}, "tuple") == (
    (1, "a"),
    (2, "b"),
    (3, "c"),
    (4, "d"),
)

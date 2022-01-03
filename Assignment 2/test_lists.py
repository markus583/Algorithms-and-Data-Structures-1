import time

from My_SingleLinkedList import MySingleLinkedList


def compare_lists(num, measurements=3, verbose=None):
    """
    :param num: Number of insertions at the beginning of a list
    :param measurements: Number of measurements to be made
    :param verbose: determines amount of text output to the console.
    None prints nothing, False prints only the difference of the averages, True prints everything.
    """
    # initiate lists
    python_list = []
    my_singly_linked_list = MySingleLinkedList()
    # set up list to store averages
    differences_pylist = []
    differences_mylist = []
    # loop over measurements/take 3 measurements
    for _ in range(measurements):
        start_time_pylist = time.time_ns()
        for iteration in range(num):
            python_list.insert(0, iteration)  # insert at start of list; could be any value instead of iteration
        end_time_pylist = time.time_ns()
        differences_pylist.append(end_time_pylist - start_time_pylist)  # store difference
        if verbose:
            print(f"Single iteration, pylist: {end_time_pylist - start_time_pylist}ns")

        start_time_mylist = time.time_ns()
        for iteration in range(num):
            my_singly_linked_list.prepend(iteration)  # insert at start of list; could be any value instead of iteration
        end_time_mylist = time.time_ns()
        differences_mylist.append(end_time_mylist - start_time_mylist)  # store difference
        if verbose:
            print(f"Single iteration, mylist: {end_time_mylist - start_time_mylist}ns")

    difference = sum(differences_pylist) / 3 - sum(differences_mylist) / 3
    if verbose:
        print(f"The built-in Python list takes on average {sum(differences_pylist) / 3}ns.")
        print(f"My implementation of a singly linked list takes on average {sum(differences_mylist) / 3}ns.")
        if difference > 0:
            print(
                f"With {num} insertions at the beginning, my implementation of a singly linked list"
                f" is {difference} ns or"
                f" {difference / 1000} us or"
                f" {difference / 1000000000} s faster than a built-in Python list."
            )
        elif difference < 0:
            print(
                f"With {num} insertions at the beginning, the built-in Python list"
                f" is {-difference}ns or"
                f" {-difference / 1000}us or"
                f" {-difference / 1000000000}s faster than my implementation of a singly linked list."
            )
    elif verbose is False:
        print(difference)
    return difference


def test_compare_lists():
    num_elements = [1_000, 10_000, 100_000, 200_000, 300_000]
    for num_element in num_elements:
        difference = compare_lists(num_element, verbose=None)  # get difference of implementations, print nothing here
        if difference > 0:  # my list is faster
            print(f"{num_element}: My_SingleLinkedList is {difference / 1000:.2f}us faster")
        elif difference < 0:  # built-in Python list is faster
            print(f"{num_element}:Built-in Python list is {-difference / 1000:.2f}us faster")

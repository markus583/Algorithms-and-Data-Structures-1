class RadixSort:
    def __init__(self):
        self.base = 7
        #                                _________list of bucketlists
        #                               | ________list of buckets -> storage_list of buckets as array here
        #                               || ___________content of a bucket -> buckets as arrays here
        #                               |||
        self.bucket_list_history = []  # [[[]]] -> will look like this in the end

    def get_bucket_list_history(self):
        return self.bucket_list_history

    def sort(self, sort_list):
        """
        Sorts a given storage_list using radixsort in ascending order
        @param sort_list to be sorted
        @returns a sorted storage_list
        @raises ValueError if the storage_list is None
        """
        self.bucket_list_history.clear()  # clear history storage_list at beginning of sorting
        if sort_list is None:
            raise ValueError

        def get_digit(some_number, n):
            """
            Get n-th digit of some number, from right (0th digit) to left (leading digit)
            """
            return some_number // 10 ** n % 10

        array = sort_list  # create copy of storage_list: again, not necessary and possibly memory-inefficient, but safer
        max_length = int(len(str(max(array))))  # get maximum length of all numbers

        for index, _ in enumerate((range(max_length))):  # eg. max. 4-digit number --> 4 iterations
            buckets = [[] for _ in range(self.base)]  # create 7 empty buckets
            for number in array:  # O(n)
                digit = get_digit(number, index)  # get digit of current number at index
                buckets[digit].append(number)  # add current number to bucket, depending on its digit

            # numbers are assigned to buckets --> append buckets to history
            self._add_bucket_list_to_history(buckets)
            # merge buckets back to storage_list
            flat_list = []
            for item in buckets:  # O(m)
                flat_list += item
            array = flat_list  # and overwrite array
        return array

    def _add_bucket_list_to_history(self, bucket_list):
        """
        This method creates a snapshot (clone) of the bucketlist and adds it to the bucketlistHistory.
        @param bucket_list is your current bucketlist, after assigning all elements to be sorted to the buckets.
        """
        arr_clone = []
        for i in range(0, len(bucket_list)):
            arr_clone.append([])
            for j in bucket_list[i]:
                arr_clone[i].append(j)

        self.bucket_list_history.append(arr_clone)

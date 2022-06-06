#global

#local
from .node import Node

class Hashset:

    """
    A large prime number used to compute a 32-bit modular hash.
    """
    HASH_PRIME = 100000000000000000000000000000000003

    """
    Maximum allowed load-factor (ratio of key-value pairs and the bucket size).
    """
    MAX_LOAD_FACTOR = 4

    def __init__(self, capacity=5):
        """
        Creates a hash set with 5 buckets by default.
        Each bucket represents the head of a linked-list, where, a linked-list
        is used for keys that have the same hash.

        :params capacity : Initial capacity of the buckets.
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity

    def __add__(self, other):
        """
        If the load capacity was greater than the allowed limit, resize the hashset to a bucket that's double
        in size to the previous one.

        :params other : a new Hashset that has bucket size double than self.
        """
        for head in self.buckets:
            while head:
                hash = head.hash
                other.buckets[hash % other.capacity] = Node(head.key, head.hash, other.buckets[hash % other.capacity])
                head = head.next
        self.buckets = []
        return other.buckets

    def __getitem__(self, key):
        hash = self.__hash(key)
        return self.__contains(self.buckets[hash % self.capacity], key)

    def __contains__(self, key):
        hash = self.__hash(key)
        return self.__contains(self.buckets[hash % self.capacity], key)

    def __delitem__(self, key):
        return self.__delete(key)

    def __iter__(self):
        for item in self.buckets:
            while item:
                yield item
                item = item.next

    def __list__(self):
        return [i.key for i in self]

    def print(self):
        for item in self.buckets:
            if item:
                while item:
                    print(f"{item.key} -> ", end="")
                    item = item.next
                print("None")


    def __hash(self, word : str):
        """
        Produces a 32-bit hash for an input string (modular hashing), using a random
        prime number that's very far-off from a power of 2.

        :params word : word to compute hash for
        """
        hash = 0
        for character in word:
            hash = hash * self.HASH_PRIME + ord(character)
        return (hash % (2**32))

    def __delete(self, key):
        """
        Deletes a key from the hash set (buckets). Raises a keyerror if the
        key was not present in the hash set.
        
        :params key : key to delete from the hash set.
        """
        hash = self.__hash(key) % self.capacity
        head = self.buckets[hash]
        if head:
            if head.key == key:
                self.buckets[hash] = self.buckets[hash].next
                self.size -= 1
                return
            while head.next:
                if head.next.key == key:
                    head.next = head.next.next
                    self.size -= 1
                    return
                head = head.next
        raise KeyError(f"{key} was not present in the hash set")

    def __contains(self, head, key):
        """
        Check if an element is present in the hash set

        :params key  : Key to check if it's already present in the hash set.
        :params head : Head of a linked list that has the same hash as key.
        """
        while head:
            if head.key == key:
                return True
            head = head.next
        return False

    def __resize(self):
        """
        Double the size of the container and copy all nodes
        to the new container.
        """
        self.capacity *= 2
        self.buckets = self + Hashset(self.capacity)

    def __check_if_resize_needed(self):
        """
        If the load factor was greater than 4, then resize the hash set to
        accomodate more data in the future.
        """
        if (self.size / self.capacity) > self.MAX_LOAD_FACTOR:
            self.__resize()


    def __prepend(self, hash, key):
        """
        Prepends a new node to the start of the linked list so as to maximize the
        performance.
        """
        self.buckets[hash % self.capacity] = Node(key, hash, self.buckets[hash % self.capacity])
        self.size += 1
        self.__check_if_resize_needed()

    def add(self, key, _hash=None):
        """
        Adds a key to the hash set (buckets). Ignores if the key was already
        present.

        :params key   : key to compute hash from and store to the hash set.
        """
        hash = _hash if _hash else self.__hash(key)
        if not self.__contains(self.buckets[hash % self.capacity], key):
            self.__prepend(hash, key)

    def union(self, other):
        """
        Elements of this hashset or in the other hashset

        :returns : new hashset that represents union of two input
                   hashsets.
        """
        new_hashset = self if self.size >= other.size else other
        iter_from = other if self.size >= other.size else self
        for item in iter_from:
            new_hashset.add(item.key, item.hash)
        return new_hashset

    def intersection(self, other):
        """
        Elements of this hashset that are also present in the other hashset

        :returns : new hashset that represents intersection of two input
                   hashsets.
        """
        new_hashset = Hashset()
        for i in self:
            if i.key in other:
                new_hashset.add(i.key, i.hash)
        for j in other:
            if j.key in self:
                new_hashset.add(j.key, j.hash)
        return new_hashset

    def and_not(self, other):
        """
        Elements of this hashset that are not present in the other hashset

        :returns : new hashset that represents 'and not' operation of two
                   input hashsets.
        """
        new_hashset = Hashset()
        for i in self:
            if i.key not in other:
                new_hashset.add(i.key, i.hash)
        return new_hashset


        
    
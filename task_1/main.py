from hashtable import HashTable

hash_table = HashTable(capacity=100)
hash_table["1"] = 1
hash_table[2] = "2"
hash_table.put("foo", "bar")

if __name__ == "__main__":
    print(hash_table.get('1'))  # 1
    print(hash_table[2])  # 2
    print(hash_table.get('foo'))  # bar
    print(hash_table)

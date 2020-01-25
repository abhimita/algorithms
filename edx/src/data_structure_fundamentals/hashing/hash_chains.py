# python3

class Query:

    def __init__(self, query):
        self.type = query[0]
        if self.type == 'check':
            self.ind = int(query[1])
        else:
            self.s = query[1]

class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        # store all strings in one list
        self.elems = [[] for i in range(bucket_count)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % self.bucket_count

    def write_search_result(self, was_found):
        print('yes' if was_found else 'no')

    def write_chain(self, chain):
        print(' '.join(chain))

    def read_query(self):
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.check(query.ind)
        elif query.type == 'add':
            self.add(query)
        elif query.type == 'del':
            self.delete(query)
        elif query.type == 'find':
            self.find(query)

    def add(self, query):
        index = self._hash_func(query.s)
        if query.s not in self.elems[index]:
            self.elems[index] = [query.s] + self.elems[index]

    def find(self, query):
        index = self._hash_func(query.s)
        self.write_search_result(True if query.s in self.elems[index] else False)

    def delete(self, query):
        index = self._hash_func(query.s)
        if query.s not in self.elems[index]:
            return
        self.elems[index].remove(query.s)

    def check(self, i):
        self.write_chain(self.elems[i])


    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.process_query(self.read_query())

if __name__ == '__main__':
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()

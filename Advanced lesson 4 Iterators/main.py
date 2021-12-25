# исходный список
nested_list = [
	['a', 'b', 'c', ['jdksj']],
	['d', 'e', 'f', 'h', False],
	[1, 2, None],
]

# задание 1 - итератор
class FlatIterator():
    def __init__(self, in_list):
        self.flat_list = list(self.flatten_list(in_list))
        self.end = len(self.flat_list)
    
    def flatten_list(self, in_list):
        # реализация для любой вложенности
        for i in in_list:
            if isinstance(i, list):
                yield from self.flatten_list(i)
            else:
                yield i

        # # реализация для изначального списка с вложенностью 2
        # flat_list = []
        # for i in in_list:
        #     flat_list.extend(i)
        # return flat_list
    
    def __iter__(self):
        self.cursor = -1
        return self
    
    def __next__(self):
        self.cursor += 1
        if self.cursor == self.end:
            raise StopIteration
        return self.flat_list[self.cursor]

for item in FlatIterator(nested_list):
	print(item) 

print('\n========\n')

# задание 2 - генератор
def flat_generator(in_list):
    def flatten_list(in_list):
        # реализация для любой вложенности
        for i in in_list:
            if isinstance(i, list):
                yield from flatten_list(i)
            else:
                yield i
        
        # реализация для изначального списка с вложенностью 2
        # flat_list = []
        # for i in in_list:
        #     flat_list.extend(i)
        # return flat_list

    cursor = 0
    flat_list = list(flatten_list(in_list))
    while cursor < len(flat_list):
        yield flat_list[cursor]
        cursor += 1

for item in  flat_generator(nested_list):
	print(item)
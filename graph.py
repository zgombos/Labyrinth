
class Graph:
    def __init__(self):
        """
        Make the following dictionary data structure:
        { a:[1,2,3],
          b:[4],
          c:[5,6,7,8] }
        """
        self.vertex_list = {}

    def add_vertex(self, node):
        if node not in self.vertex_list:
            self.vertex_list[node] = []

    def add_edge(self, src, dst):
        self.vertex_list[src].append(dst)

    def get_vertex(self):
        return self.vertex_list

    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.vertex_list:
            return None
        for node in self.vertex_list[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath:
                    return newpath
        return None

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.vertex_list:
            return []
        paths = []
        for node in self.vertex_list[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.vertex_list:
            return None
        shortest = None
        for node in self.vertex_list[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


if __name__ == '__main__':
    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b')
    g.add_edge('a', 'c')
    g.add_edge('a', 'f')
    g.add_edge('b', 'c')
    g.add_edge('b', 'd')
    g.add_edge('c', 'd')
    g.add_edge('c', 'f')
    g.add_edge('d', 'e')
    g.add_edge('e', 'f')

    print(g.vertex_list)
    for v in g.vertex_list:
        print('Vertex:', v)
    print('Path:', g.find_path('a', 'd'))
    print('All path:', g.find_all_paths('a', 'd'))
    print('Shortest:', g.find_shortest_path('a', 'd'))

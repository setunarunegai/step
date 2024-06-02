import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        #start and goal change to id
        there_key = False
        for id in self.titles.keys():
            if self.titles[id] == start:
                start = id
                there_key = True
                break
        if there_key == False:
            print("There isn't start page")
            return 0
        there_key = False
        for id in self.titles.keys():
            if self.titles[id] == goal:
                goal = id
                there_key = True
                break
        if there_key == False:
            print("There isn't goal page")
            return 0
        if start == goal:
            print("The shortest path pages are:")
            print([self.titles[start]])
            print()
            return 0
        queue = deque() #add:append, delete:popleft
        visited = {}
        visited[start] = start
        queue.append(start)
        shortest_path = []
        while len(queue)>0:
            node = queue.popleft()
            if node == goal:
                #path from goal to start
                before = node
                shortest_path.append(self.titles[node])
                while before != start:
                    before = visited[before]
                    shortest_path.append(self.titles[before])
                shortest_path.reverse()
                print("The shortest path pages are:")
                print(shortest_path)
                print()
                return 0
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = node
                    queue.append(child)
        print("The path is none")
        print()

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pagerank = {}
        new_pagerank = {}
        for id in self.titles.keys():
            pagerank[id] = 1.0
            new_pagerank[id] = 0.0
        number_page = float(len(pagerank))
        distance = number_page
        while distance > number_page*0.001:
            for id in self.titles.keys():
                if id in self.links.keys():
                    links = pagerank[id]*(0.8500/float(len(self.links[id]))+0.1500/number_page)
                    others = pagerank[id]*0.1500/number_page
                    for id_id in self.titles.keys():
                        if id_id in self.links[id]:
                            new_pagerank[id_id] += links
                        else:
                            new_pagerank[id_id] += others
                else:
                    others = pagerank[id]/number_page
                    for id_id in self.titles.keys():
                        new_pagerank[id_id] += others
            distance = 0.0
            for id in self.titles.keys():
                distance += abs(new_pagerank[id]-pagerank[id])
                pagerank[id] = new_pagerank[id]
                new_pagerank[id] = 0.0
        print("The popular pages are:")
        highrank = sorted(pagerank.items(), key=lambda x:x[1], reverse=True)
        index = 0
        while index < 10 and index < len(highrank):
            print(self.titles[highrank[index][0]])
            index += 1
        print()


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    #wikipedia.find_shortest_path('A', 'E')
    wikipedia.find_most_popular_pages()

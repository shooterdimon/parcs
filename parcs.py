from Pyro4 import expose
import random
import time


class Solver:
    def __init__(self, workers=None, in_file_path=None, out_file_path=None):
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path
        self.workers = workers
        self.labirint = []
        self.N = 0
        self.M = 0
        self.K = 0
        print("Initialized")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        (self.N, self.M, self.K, self.labirint) = self.read_input()

        start_time = time.time()

        count = (self.K + len(self.workers) -1) / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(str(self.N), str(self.M), str(count), self.labirint))

        # reduce
        way = self.myreduce(mapped)

        if len(way) == 0:
            self.write_output("", [])

        self.prepareToOutput(way)

        end_time = time.time()
        # output
        self.write_output(self.labirint, way, end_time-start_time)

        print("Job Finished")

    def prepareToOutput(self, way):
        for i in range(1, len(way)):
            self.labirint[way[i][0]] = self.labirint[way[i][0]][:way[i][1]] + '*' + self.labirint[way[i][0]][way[i][1]+1:]

        return

    @staticmethod
    @expose
    def mymap(N, M, K, labirint):
        N = int(N)
        M = int(M)
        K = int(K)

        output = []

        for i in range(K):
            result = Solver.brootforce(N, M, labirint)

            if result[0] == 1:
                if len(output) == 0 or len(output) > len(result):
                    output = result

        return output

    @staticmethod
    @expose
    def brootforce(N, M, labirint):
        positionX = 0
        positionY = 0

        makingMoves = [0, [0, 0]]

        for i in range(10000):
            if positionX == N-1 and positionY == M-1:
                makingMoves[0] = 1
                return makingMoves

            possibleMoves = []

            if positionX > 0 and labirint[positionX-1][positionY] == '.' and makingMoves[len(makingMoves)-2] != [positionX-1, positionY]:
                possibleMoves.append([positionX-1, positionY])

            if positionY > 0 and labirint[positionX][positionY-1] == '.' and makingMoves[len(makingMoves)-2] != [positionX, positionY-1]:
                possibleMoves.append([positionX, positionY-1])

            if positionX < N-1 and labirint[positionX+1][positionY] == '.' and makingMoves[len(makingMoves)-2] != [positionX+1, positionY]:
                possibleMoves.append([positionX+1, positionY])

            if positionY < M-1 and labirint[positionX][positionY+1] == '.' and makingMoves[len(makingMoves)-2] != [positionX, positionY+1]:
                possibleMoves.append([positionX, positionY+1])

            if len(possibleMoves) == 0:
                positionX = makingMoves[len(makingMoves)-2][0]
                positionY = makingMoves[len(makingMoves)-2][1]
                makingMoves.append([positionX, positionY])
            else:
                val = random.randint(0, len(possibleMoves)-1)
                makingMoves.append(possibleMoves[val])
                positionX = possibleMoves[val][0]
                positionY = possibleMoves[val][1]

        return makingMoves

    @staticmethod
    @expose
    def myreduce(mapped):
        print("Reducing")
        output = []

        for way in mapped:
            if way.value[0] == 1:
                if len(output) == 0 or len(output) > len(way.value):
                    output = way.value

        print("Reducing complete")
        return output

    def read_input(self):
        f = open(self.in_file_path, 'r')
        n = int(f.readline())
        m = int(f.readline())
        k = int(f.readline())

        labirint = []

        for i in range(n):
            line = f.readline()
            labirint.append(line)

        f.close()
        return n, m, k, labirint

    def write_output(self, output, way, timer):
        f = open(self.out_file_path, 'w')

        if len(way) == 0:
            f.write("Sorry, we didn`t find the way")
            f.close()
            return

        f.write("Shortest found way:\n")

        for i in range(1, len(way)):
            f.write(str(way[i]) + " -> ")

        f.write("Done!\n\nResults:\n")

        for i in range(len(output)):
            f.write(output[i])

        f.write("\n\nTime spend to complete the job:")
        f.write(str(timer))

        f.close()
        print("Output saved")
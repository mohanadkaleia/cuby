import copy
import argparse
import numpy as np

from enum import Enum


class Direction(Enum):
    Forward = 'f'
    Reverse = 'r'


class Cell:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color


class Face:
    def __init__(self, size, color, label):
        self.size = size
        self.label = label
        self.face = np.array(
            [[Cell(f'{i+1}{j+1} {color}') for j in range(size)] for i in range(size)])
        self.adjacent = self._get_adjacent()

    def __repr__(self):
        face_str = []
        for row in self.face:
            for col in row:
                face_str.append(str(col))
            face_str.append("\n")

        # return face_str
        return ' ' + ' '.join(face_str)

    def _get_adjacent(self):
        '''
        Neighborhood faces are organized in 1d list:
        [Upper side, down side, right side, left side]
        '''
        # Front side
        if self.label == 'f':
            return ['u', 'd', 'r', 'l']
        # Right side
        elif self.label == 'r':
            return ['u', 'd', 'b', 'f']
        # Left side
        elif self.label == 'l':
            return ['u', 'd', 'f', 'b']
        # Back side
        elif self.label == 'b':
            return ['u', 'd', 'l', 'r']
        # Up side
        elif self.label == 'u':
            return ['b', 'f', 'r', 'l']
        # Down side
        elif self.label == 'd':
            return ['f', 'b', 'r', 'l']

    def __getitem__(self, key):
        return self.face[key]

    def __setitem__(self, idx, value):
        self.face[idx] = value


class Cube:
    def __init__(self, size):
        self.size = size
        self.front = Face(size, 'green', 'f')
        self.back = Face(size, 'blue', 'b')
        self.right = Face(size, 'red', 'r')
        self.left = Face(size, 'orange', 'l')
        self.down = Face(size, 'yellow', 'd')
        self.up = Face(size, 'white', 'u')

    def rotate(self, action, direction):
        if action == 'u':
            self._rotate_face(self.up, direction)
            self._rotate_adjacent(self.up, direction)
            print('Rotating..',)
        elif action == 'd':
            self._rotate_face(self.down, direction)
            self._rotate_adjacent(self.down, direction)
            print('Rotating..')
        elif action == 'l':
            self._rotate_face(self.left, direction)
            self._rotate_adjacent(self.left, direction)
            print('Rotating..')
        elif action == 'r':
            self._rotate_face(self.right, direction)
            self._rotate_adjacent(self.right, direction)
            print('Rotating..')
        elif action == 'f':
            self._rotate_face(self.front, direction)
            self._rotate_adjacent(self.front, direction)
            print('Rotating..')
        elif action == 'b':
            self._rotate_face(self.back, direction)
            self._rotate_adjacent(self.back, direction)
            print('Rotating..')

    def _rotate_face(self, face, direction):
        # Trick to rotate in reverse direction
        # just rotate 3 times in the forward
        num_of_rotation = 1 if direction.value == 'f' else 3
        for _ in range(num_of_rotation):
            rotated = copy.deepcopy(face)
            for i in range(self.size):
                for j in range(self.size):
                    rotated[i][j] = face[self.size - 1 - j][i]
            face = rotated

    def _map_face(self, label):
        if label == 'u':
            return self.up
        elif label == 'd':
            return self.down
        elif label == 'l':
            return self.left
        elif label == 'r':
            return self.right
        elif label == 'f':
            return self.front
        elif label == 'b':
            return self.back

    def _rotate_adjacent(self, face, direction):
        adjacent = face.adjacent
        upper_face = self._map_face(adjacent[0])
        down_face = self._map_face(adjacent[1])
        right_face = self._map_face(adjacent[2])
        left_face = self._map_face(adjacent[3])

        # Trick to rotate in reverse direction
        # just rotate 3 times in the forward
        num_of_rotation = 1 if direction.value == 'f' else 3
        for _ in range(num_of_rotation):
            # Rotate adjacent faces
            if face.label == 'f':
                tmp1 = copy.copy(right_face[:, 0])
                right_face[:, 0] = upper_face[self.size - 1]

                tmp2 = copy.copy(down_face[0])
                down_face[0] = tmp1

                tmp3 = copy.copy(left_face[:, self.size - 1])
                left_face[:, self.size - 1] = tmp2

                upper_face[self.size - 1] = tmp3

            elif face.label == 'r':
                tmp1 = copy.copy(right_face[:, 0])
                right_face[:, 0] = upper_face[:, self.size - 1]

                tmp2 = copy.copy(down_face[:, self.size - 1])
                down_face[:, self.size - 1] = tmp1

                tmp3 = copy.copy(left_face[:, self.size - 1])
                left_face[:, self.size - 1] = tmp2

                upper_face[:, self.size - 1] = tmp3

            elif face.label == 'l':
                tmp1 = copy.copy(right_face[:, 0])
                right_face[:, 0] = upper_face[:, 0]

                tmp2 = copy.copy(down_face[:, 0])
                down_face[:, 0] = tmp1

                tmp3 = copy.copy(left_face[:, self.size - 1])
                left_face[:, self.size - 1] = tmp2

                upper_face[:, 0] = tmp3

            elif face.label == 'b':
                tmp1 = copy.copy(right_face[:, 0])
                right_face[:, 0] = upper_face[0]

                tmp2 = copy.copy(down_face[self.size - 1])
                down_face[self.size - 1] = tmp1

                tmp3 = copy.copy(left_face[:, self.size - 1])
                left_face[:, self.size - 1] = tmp2

                upper_face[0] = tmp3

            elif face.label == 'u':
                tmp1 = copy.copy(right_face[:, 0])
                right_face[:, 0] = upper_face[0]

                tmp2 = copy.copy(down_face[self.size - 1])
                down_face[self.size - 1] = tmp1

                tmp3 = copy.copy(left_face[:, self.size - 1])
                left_face[:, self.size - 1] = tmp2

                upper_face[0] = tmp3

            elif face.label == 'd':
                tmp1 = copy.copy(right_face[self.size - 1])
                right_face[self.size - 1] = upper_face[self.size - 1]

                tmp2 = copy.copy(down_face[self.size - 1])
                down_face[self.size - 1] = tmp1

                tmp3 = copy.copy(left_face[self.size - 1])
                left_face[self.size - 1] = tmp2

                upper_face[self.size - 1] = tmp3


def main():
    parser = argparse.ArgumentParser(description='Rubike\'s cube')
    parser.add_argument('--direction', '-d', default='f',
                        help='Rotate the cube in direction [f: forward, r: reverse]')
    parser.add_argument('--face', '-f', default='f',
                        help='Rotate face [f, b, l ,r, u, d]')
    parser.add_argument('--size', '-z', type=int, default=3,
                        help='Cube size, default 3')

    args = vars(parser.parse_args())
    direction = args['direction']
    face = args['face']
    size = args['size']

    print(
        f'Creating a cube of size {size} and rotate face {face} in direction {direction}')
    cube = Cube(size)
    cube.rotate(face, Direction.Reverse if direction ==
                'r' else Direction.Forward)

    print("Front")
    print(cube.front)

    print("Upper")
    print(cube.up)

    print("Down")
    print(cube.down)

    print("Right")
    print(cube.right)

    print("Left")
    print(cube.left)

    print("Back")
    print(cube.back)


if __name__ == "__main__":
    # while True:
    main()

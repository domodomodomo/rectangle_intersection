from rectangle_intersection import Rectangle
from rectangle_intersection import RectangleList
from rectangle_intersection import RectangleBinaryTree
from rectangle_intersection import RectangleQuadTree
import random
import time


def sample_code():
    region = Rectangle(0, 0, 100000, 100000)

    sample_rectangle_list = generate_sample_rectangle_list(
        num_of_rectangle=100,
        average_length_of_one_side=100,
        region=region)

    query_rectangle = Rectangle(50, 50, 100, 100)

    #
    # 1) RectangleList
    #
    rectangle_set = RectangleList(region)

    print(type(rectangle_set).__name__)
    # extend
    start_time = time.time()
    rectangle_set.extend(sample_rectangle_list)
    end_time = time.time()
    execution_time = end_time - start_time
    print('extend:', execution_time)

    # stub
    start_time = time.time()
    query_result = rectangle_set.stub(query_rectangle)
    end_time = time.time()
    execution_time = end_time - start_time
    print('stub:  ', execution_time)

    #
    # 2) RectangleBinaryTree
    #
    rectangle_set = RectangleBinaryTree(region, 8)

    print(type(rectangle_set).__name__)
    # extend
    start_time = time.time()
    rectangle_set.extend(sample_rectangle_list)
    end_time = time.time()
    execution_time = end_time - start_time
    print('extend:', execution_time)

    # stub
    start_time = time.time()
    query_result = rectangle_set.stub(query_rectangle)
    end_time = time.time()
    execution_time = end_time - start_time
    print('stub:  ', execution_time)

    #
    # 3) RectangleQuadTree
    #
    rectangle_set = RectangleQuadTree(region, 4)

    print(type(rectangle_set).__name__)
    # extend
    start_time = time.time()
    rectangle_set.extend(sample_rectangle_list)
    end_time = time.time()
    execution_time = end_time - start_time
    print('extend:', execution_time)

    # stub
    start_time = time.time()
    query_result = rectangle_set.stub(query_rectangle)
    end_time = time.time()
    execution_time = end_time - start_time
    print('stub:  ', execution_time)

    # through away result
    query_result


def generate_sample_rectangle_list(
        num_of_rectangle, average_length_of_one_side, region):
    average_length = average_length_of_one_side
    # print(average_side)
    # exit()
    sigma = average_length // 3
    rectangle_list = []
    k = 0
    while k <= num_of_rectangle:
        x1 = random.randint(region.x1, region.x2)
        y1 = random.randint(region.y1, region.y2)
        x2 = x1 + abs(int(random.normalvariate(average_length, sigma)))
        y2 = y1 + abs(int(random.normalvariate(average_length, sigma)))
        rectangle = Rectangle(x1, y1, x2, y2)
        # print(rectangle)
        if rectangle <= region:
            rectangle_list.append(rectangle)
            k += 1
    return rectangle_list


sample_code()

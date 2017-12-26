### rectangle intersection
This codes implements 2D rectangle stub query and provides follwoing three data structures.

|No.|Class Name|Description|
|:----:|:----|:----|
|1.|RectangleList|List|
|2.|RectangleBinaryTree|Binary Tree|
|3.|RectangleQuadTree|Linear Quad Tree with Morton Order|

<br>
This code consider that two rectangles have intersection, when two rectangles are tangent each other,<br>
such as Rectangle(0, 0, 10, 10) and Rectangle(10, 5, 25, 15).

<br>

### usage
#### rectangle\_intersection.py
stub query
```python
>>> from rectangle_intersection import *
>>> 
>>> # 1) Initialize.
>>> region = Rectangle(0, 0, 100, 100)
>>> rectangle_set = RectangleList(region)
>>> # rectangle_set = RectangleBinaryTree(region, height=4)
>>> # rectangle_set = RectangleQuadTree(region, height=2)
>>> 
>>> # 2) Add rectangles.
>>> rectangle_list = [Rectangle(10, 10, 20, 20), Rectangle(20, 20, 40, 40)]
>>> rectangle_set.extend(rectangle_list)
>>> 
>>> # 3) Stub rectangle.
>>> query_rectangle = Rectangle(5, 5, 15, 15)
>>> rectangle_set.stub(query_rectangle)
[Rectangle(10, 10, 20, 20)]
>>>
```

<br>

#### sample.py
sample.py is codes to show you benchmark of each data structure.<br>

sample.py adds 100 rectangles, do stub-query 1 time,<br>
and show you execution times of adding rectangles(extend) and stub-query(stub) for each data structure.

```
$ python sample.py
RectangleList
extend: 0.00011205673217773438
stub:   0.00016999244689941406
RectangleBinaryTree
extend: 0.004693031311035156
stub:   6.985664367675781e-05
RectangleQuadTree
extend: 0.0009031295776367188
stub:   2.9087066650390625e-05
$
```

##### 1. extend cost
RectangleList is faster, comparing with others, RectangleBinaryTree, RectangleQuadTree.

##### 2. stub cost
RectangleBinaryTree and RectangleQuadTree is faster than RectangleList.

<br>

#### sample2.py
rectangle\_intersection.py also supports set operations.<br>
sample2.py shows you how the set operations work.

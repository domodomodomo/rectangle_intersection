"""Sample code for set operations."""
from rectangle_intersection import Rectangle
from rectangle_intersection import RectangleList
from rectangle_intersection import RectangleBinaryTree
from rectangle_intersection import RectangleQuadTree

#
# Initialize
#
region = Rectangle(0, 0, 100, 100)

rectangle_list = RectangleList(region)
rectangle_list.extend([Rectangle(10, 10, 20, 20), Rectangle(20, 20, 40, 40)])

rectangle_binary_tree = RectangleBinaryTree(region, height=4)
rectangle_binary_tree.extend([Rectangle(10, 10, 20, 20)])

rectangle_quad_tree = RectangleQuadTree(region, height=2)
rectangle_quad_tree.extend([Rectangle(20, 20, 40, 40)])


#
# sample codes.
#
for rectangle in rectangle_list:
    print(rectangle)

rectangle_list == rectangle_binary_tree

rectangle_list = rectangle_list - rectangle_quad_tree

print(rectangle_list)
print(rectangle_binary_tree)

rectangle_list == rectangle_binary_tree

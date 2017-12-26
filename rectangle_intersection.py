#
# Rctangle class
#


# @immutable
class Rectangle(object):
    def __init__(self, x1, y1, x2, y2):
        if not(x1 <= x2 and y1 <= y2):
            raise ValueError("Coordinates are invalid.")

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

        width_0 = (x1 - x2 == 0)
        height_0 = (y1 - y2 == 0)

        # self.is_rectangle = not witdh_0 and not height_0  # 0 0
        self.is_line = width_0 != height_0  # 0 1, 1 0 xor
        self.is_dot = width_0 & height_0  # 1 1

    def __and__(self, other):
        """Return intersection region."""
        a, b = self, other
        x1 = a.x1 if a.x1 > b.x1 else b.x1
        y1 = a.y1 if a.y1 > b.y1 else b.y1
        x2 = a.x2 if a.x2 < b.x2 else b.x2
        y2 = a.y2 if a.y2 < b.y2 else b.y2

        if x1 <= x2 and y1 <= y2:
            return type(self)(x1, y1, x2, y2)
        else:
            return None

    def __le__(self, other):
        """Check whether other rectangle are included by self, or not."""
        a, b = self, other
        return \
            a.x1 >= b.x1 and \
            a.y1 >= b.y1 and \
            a.x2 <= b.x2 and \
            a.y2 <= b.y2

    def __repr__(self):
        tuple_self = (self.x1, self.y1, self.x2, self.y2)
        return type(self).__name__ + repr(tuple_self)

    if __debug__:
        def __eq__(self, other):
            a, b = self, other
            return \
                a.x1 == b.x1 and \
                a.y1 == b.y1 and \
                a.x2 == b.x2 and \
                a.y2 == b.y2


#
# RectangleSet
#

# @abstruct
class RectangleSet(object):
    """Set of rectangles.

    This class is general-purpose class which provides two general methods,
    stub and append.
    """

    # @abstruct
    def __init__(self, region):
        """Initialize instance object.

        1) The instance's coverage area is region.
        2) An actual set of rectangles is assinged to 'self._data'.
        3) The value name "self._data" would be changed in each subclass,
            such as _tree, _rectangle_list, _board.
            Reason
            1) "self._data" is not readable.
            2) There would be no common codes for self._data in each subclass,
               because each subclass uses different algorithms.
        """
        self.region = region
        self._data = None
        raise NotImplementedError

    # @abstruct
    def stub(self, query_rectangle):
        """Pop out rectangles which overlap with query_rectangle."""
        if not query_rectangle <= self.region:
            raise ValueError("query_rectangle is out of region.")
        raise NotImplementedError

    # @abstruct
    def append(self, rectangle):
        """Add a rectangle to RectangleSet."""
        if not rectangle <= self.region:
            raise ValueError("rectangle is out of region.")
        raise NotImplementedError

    # @abstruct
    def list(self):
        """Generate "rectangle list" from "rectangel set"."""
        raise NotImplementedError

    #
    #
    #
    def extend(self, rectangle_list):
        for rectangle in rectangle_list:
            self.append(rectangle)
        # list comprehension is not faster than above...
        # [self.append(rectangle) for rectangle in rectangle_list]

    #
    # test codes
    #
    if __debug__:
        # @abstruct
        def _copy_empty(self):
            """Copy itself except _data. This method used by __sub__ method."""
            raise NotImplementedError

        def __iter__(self):
            """Make this set iterable for each rectangle contained by this."""
            return iter(self.list())

        def __len__(self):
            """Return the number of rectangles in this set."""
            return len(self.list())

        def __sub__(self, other):
            """Return sub set of self and other."""
            sub_rectangle_list = _sub(self.list(), other.list())
            sub_rectangle_set = self._copy_empty()
            sub_rectangle_set.extend(sub_rectangle_list)
            return sub_rectangle_set

        def __eq__(self, other):
            """Check two rectangle set is same or not."""
            return _equal(self.list(), other.list())

        def __str__(self):
            """Return string of class name and elements."""
            return type(self).__name__ \
                + ': ' + ', '.join(map(str, self.list()))


if __debug__:
    def _sub(lst1, lst2):
        lst1 = lst1.copy()
        lst2 = lst2.copy()
        for element in lst2:
            if element in lst1:
                lst1.remove(element)
        return lst1

    def _equal(lst1, lst2):
        lst1 = lst1.copy()
        lst2 = lst2.copy()
        # lst2 - lst1
        for element in lst2:
            exists = _remove(lst1, element)
            if not exists:
                return False
        if lst1:
            return False
        return True

    def _remove(lst, element):
        new_lst = []
        element_exists = False
        while lst:
            e = lst.pop()
            if e == element:
                del e
                element_exists = True
                break
            else:
                new_lst.append(e)
        new_lst.reverse()
        lst.extend(new_lst)
        del new_lst
        return element_exists


#
#
#
class RectangleList(RectangleSet):
    """list of rectangle class, providing linear search methods."""

    # @overrides
    def __init__(self, region):
        self.region = region
        self._rectangle_list = []

    # @overrides
    def stub(self, query_rectangle):
        if not query_rectangle <= self.region:
            raise ValueError("query_rectangle is out of region.")
        return _stub_rectangle_list(self._rectangle_list, query_rectangle)

    # @overrides
    def append(self, rectangle):
        if not rectangle <= self.region:
            raise ValueError("rectangle is out of region.")
        self._rectangle_list.append(rectangle)

    # @overrides
    def list(self):
        return self._rectangle_list.copy()

    if __debug__:
        def _copy_empty(self):
            return type(self)(region=self.region)


def _stub_rectangle_list(rectangle_list, query_rectangle):
    """Pop rectangles overlapped by query_rectangle from rectangle_list."""
    new_rectangle_list = []
    stubbed_rectangle_list = []
    while rectangle_list:
        rectangle = rectangle_list.pop()
        if rectangle & query_rectangle:
            stubbed_rectangle_list.append(rectangle)
        else:
            new_rectangle_list.append(rectangle)
    rectangle_list.extend(new_rectangle_list)
    return stubbed_rectangle_list
    """
    ###another implementation using list comprehension.
    ###It's slower than the above code, but more readable.
    new_rectangle_list \
        = [rec for rec in rectangle_list if not (rec & query_rectangle)]
    stubbded_rectangle_list \
        = [rec for rec in rectangle_list if rec & query_rectangle]

    # rectangle_list <- new_rectangle_list
    rectangle_list.clear()
    rectangle_list.extend(new_rectangle_list)

    return stubbded_rectangle_list
    """


#
#
#
class RectangleBinaryTree(RectangleSet):
    """Two Dimention Binary Tree.

    properties
    The tree structure                     static
    The insertion and deletion operation   dynamic
    """

    # @overrides
    def __init__(self, region, height, parent=None):
        self.region = region
        self.height = height
        self.parent = parent

        self._center_list = []
        self._left_tree = None
        self._right_tree = None

        if self._is_leaf():
            pass
        else:
            devided_region1, devided_region2 = self._get_devided_region()
            self._left_tree = RectangleBinaryTree(
                devided_region1, height - 1, self)
            self._right_tree = RectangleBinaryTree(
                devided_region2, height - 1, self)

    # @overrides
    def stub(self, query_rectangle):
        if not query_rectangle <= self.region and self._is_root():
            raise ValueError("query_rectangle is out of region.")

        stubbed_rectangle_list = []

        # stub 1
        stubbed_rectangle_list.extend(
            _stub_rectangle_list(self._center_list, query_rectangle))

        if self._is_leaf():
            pass
        else:
            # stub 2
            overlap1 = query_rectangle & self._left_tree.region
            if overlap1:
                stubbed_rectangle_list.extend(
                    self._left_tree.stub(query_rectangle))

            # stub 3
            overlap2 = query_rectangle & self._right_tree.region
            if overlap2:
                stubbed_rectangle_list.extend(
                    self._right_tree.stub(query_rectangle))

        return stubbed_rectangle_list

    # @overrides
    def append(self, rectangle):
        if not rectangle <= self.region:
            raise ValueError("rectangle is out of region.")

        if self._is_leaf():
            self._center_list.append(rectangle)
        else:
            overlap1 = rectangle & self._left_tree.region
            overlap2 = rectangle & self._right_tree.region
            # if not overlap1 and not overlap2:
            #     raise ValueError('The rectangle is out of the region.')
            if not overlap1 and overlap2:
                self._right_tree.append(rectangle)
            elif overlap1 and not overlap2:
                self._left_tree.append(rectangle)
            elif overlap1 and overlap2:
                self._center_list.append(rectangle)

    # @overrides
    def list(self):
        """Get all rectangles by depth-first search."""
        rectangle_list = self._center_list.copy()
        if self._left_tree:
            rectangle_list.extend(self._left_tree.list())
        if self._right_tree:
            rectangle_list.extend(self._right_tree.list())
        return rectangle_list

    #
    #
    #
    def _get_devided_region(self):
        region_width = self.region.x2 - self.region.x1
        region_height = self.region.y2 - self.region.y1

        if region_width >= region_height:
            return self._get_holizontally_devided_region()
        else:
            return self._get_vertically_devided_region()

    def _get_holizontally_devided_region(self):
        r = self.region

        length = r.x2 - r.x1
        half_length = length // 2
        # mid point
        midp = r.x1 + half_length
        # right_side
        # left_side
        region1 = Rectangle(midp, r.y1, r.x2, r.y2)
        region2 = Rectangle(r.x1, r.y1, midp, r.y2)

        return region1, region2

    def _get_vertically_devided_region(self):
        r = self.region

        length = r.y2 - r.y1
        half_length = length // 2
        # mid point
        midp = r.y1 + half_length
        # upper side
        # lower side
        region1 = Rectangle(r.x1, midp, r.x2, r.y2)
        region2 = Rectangle(r.x1, r.y1, r.x2, midp)

        return region1, region2

    def _is_leaf(self):
        return self.height == 0

    def _is_root(self):
        return self.parent is None

    #
    #
    #
    if __debug__:
        def _copy_empty(self):
            return type(self)(region=self.region, height=self.height)


#
#
#
class RectangleQuadTree(RectangleSet):
    """linear quad tree with morton order.

    ###Two Tricks
    1) Morton Order
    2) Linear Quad Tree
    https://sbfl.net/blog/2017/12/03/javascript-collision/#i-8
    """

    # @overrides
    def __init__(self, region, height):
        len_nodes = _sum_quad_geometric_progression(self.height + 1)
        x_length = self.region.x2 - self.region.x1
        y_length = self.region.y2 - self.region.y1

        #
        self.region = region
        self.height = height
        self._linear_quad_tree = [[] for i in range(len_nodes)]

        #
        self.devided_x_side = - (-x_length // (2 ** self.height))
        self.devided_y_side = - (-y_length // (2 ** self.height))

    # @override
    def stub(self, query_rectangle):
        if not query_rectangle <= self.region:
            raise ValueError("query_rectangle is out of region.")
        stubbed_rectangle_list = []
        for intersection_index \
                in self._intersection_index_list(query_rectangle):
            linear_quad_subtree = self._linear_quad_tree[intersection_index]
            stubbed_rectangle_list.extend(
                _stub_rectangle_list(linear_quad_subtree, query_rectangle))
        return stubbed_rectangle_list

    # @overrides
    def append(self, rectangle):
        if not rectangle <= self.region:
            raise ValueError("rectangle is out of region.")
        index = self._inclusion_index(rectangle)
        linear_quad_subtree = self._linear_quad_tree[index]
        linear_quad_subtree.append(rectangle)

    # @overrides
    def list(self):
        rectangle_list = []
        for rectangle_list_contained_by_region in self._linear_quad_tree:
            rectangle_list.extend(rectangle_list_contained_by_region)
        return rectangle_list

    #
    #
    #
    def _inclusion_index(self, rectangle):
        """Calc liner quad tree index, rectangle belongs to."""
        morton_number, depth = self._calc_morton_number(rectangle)
        return type(self)._index(depth, morton_number)

    @staticmethod
    def _index(depth, morton_number):
        len_ancestor_nodes = _sum_quad_geometric_progression(depth)
        inclusion_index = len_ancestor_nodes + morton_number
        return inclusion_index

    def _calc_morton_number(self, rectangle):
        #
        # Calc lower left and upper right morton number
        #
        cell_x1 = rectangle.x1 // self.devided_x_side
        cell_y1 = rectangle.y1 // self.devided_y_side
        cell_x2 = rectangle.x2 // self.devided_x_side
        cell_y2 = rectangle.y2 // self.devided_y_side

        # bounday
        #   If the rectangle's lower or bottom side is tangent
        #   with side of cell, then
        #   move the cell to upper or left cell.
        if rectangle.x2 % self.devided_x_side == 0:
            cell_x2 -= 1
        if rectangle.y2 % self.devided_y_side == 0:
            cell_y2 -= 1

        lower_left_morton_number \
            = _separated32bit(cell_x1) | _separated32bit(cell_y1) << 1
        upper_right_morton_number \
            = _separated32bit(cell_x2) | _separated32bit(cell_y2) << 1

        #
        # Calc height and depth
        #
        if lower_left_morton_number == upper_right_morton_number:
            height = 0
            depth = self.height
        else:
            xor_ = lower_left_morton_number ^ upper_right_morton_number
            for depth in range(self.height + 1):
                # difference
                height = self.height - depth
                difference = (xor_ >> (height * 2)) & 0b11

                # tangent
                # boundary
                #   If the rectangle is tangent with side of cell, then
                #   append the rectangle to upper depth of cell.
                #   This is because, this code consider two rectangle with
                #   tangent each other has intersection.
                tangent = \
                    rectangle.x1 % self.devided_x_side or \
                    rectangle.y1 % self.devided_y_side or \
                    rectangle.x2 % self.devided_x_side or \
                    rectangle.y2 % self.devided_y_side

                #
                if difference or tangent:
                    # Even though difference will not be 0 at depth 0,
                    # rectangle might be tangent with side at depth 0.
                    if depth == 0:
                        height = height
                        depth = depth
                    else:
                        height = height + 1
                        depth = depth - 1
                    break

        #
        # Calc Morton number
        #
        morton_number = lower_left_morton_number >> (height * 2)
        return morton_number, depth

    def _intersection_index_list(self, rectangle):
        """Get index list of self.linear_quad_tree."""
        intersection_index_list = []
        base_morton_number, base_depth = self._calc_morton_number(rectangle)

        # 1)
        for depth in range(0, base_depth + 1):
            height = base_depth - depth
            morton_number = base_morton_number >> (height * 2)
            index = type(self)._index(depth, morton_number)
            intersection_index_list.append(index)

        # 2)
        max_depth = self.height
        for depth in range(base_depth + 1, max_depth + 1):
            height = - (base_depth - depth)
            prefix = base_morton_number << (height * 2)
            suffix = -1
            while True:
                suffix += 1
                morton_number = prefix + suffix
                index = type(self)._index(depth, morton_number)
                intersection_index_list.append(index)
                if suffix == 4 ** height - 1:
                    break
        return intersection_index_list

    #
    #
    #
    if __debug__:
        def _copy_empty(self):
            return type(self)(region=self.region, height=self.height)


def _sum_quad_geometric_progression(n):
    return (4 ** n - 1) // (4 - 1)


def _separated32bit(n):
    #                     0babcdefghijklmnopabcedfghijklmnop
    n = (n | (n << 16)) & 0b00000000000000001111111111111111
    #                    0b00000000abcedfghabcedfghijklmnop
    n = (n | (n << 8)) & 0b00000000111111110000000011111111
    #                    0b0000abcdefghefgh0000ijkl0000mnop
    n = (n | (n << 4)) & 0b00001111000011110000111100001111
    #                    0b00ab00cd00ef00gh00ij00kl00mn00op
    n = (n | (n << 2)) & 0b00110011001100110011001100110011
    #                    0b0a0b0c0d0e0f0g0h0i0j0k0l0m0n0o0p
    n = (n | (n << 1)) & 0b01010101010101010101010101010101
    return n

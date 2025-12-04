# CourseCatalog.py

from CourseCatalogNode import CourseCatalogNode


class CourseCatalog:
    """Binary Search Tree storing CourseCatalogNode objects."""

    def __init__(self):
        # Lab spec: only one attribute root
        self.root = None

    # ---------- internal helpers ----------

    def _compare_key(self, department, courseId, node):
        """Compare (department, courseId) with node's key; return -1/0/1."""
        dept = department.upper()
        if dept < node.department:
            return -1
        if dept > node.department:
            return 1
        if courseId < node.courseId:
            return -1
        if courseId > node.courseId:
            return 1
        return 0

    def _find_node(self, department, courseId):
        """Find node by (department, courseId); return None if not found."""
        dept = department.upper()
        cur = self.root
        while cur is not None:
            cmp = self._compare_key(dept, courseId, cur)
            if cmp == 0:
                return cur
            elif cmp < 0:
                cur = cur.left
            else:
                cur = cur.right
        return None

    # ---------- public methods ----------

    def addCourse(self, department, courseId, courseName, lecture, sections):
        """
        Insert a course into the BST.

        If a course with same (department, courseId) already exists,
        do nothing and return False. Otherwise insert and return True.
        """
        dept = department.upper()
        new_node = CourseCatalogNode(dept, courseId, courseName, lecture, sections)

        if self.root is None:
            self.root = new_node
            return True

        cur = self.root
        parent = None
        while cur is not None:
            parent = cur
            cmp = self._compare_key(dept, courseId, cur)
            if cmp == 0:
                # duplicate key
                return False
            elif cmp < 0:
                cur = cur.left
            else:
                cur = cur.right

        new_node.parent = parent
        if self._compare_key(dept, courseId, parent) < 0:
            parent.left = new_node
        else:
            parent.right = new_node

        return True

    def addSection(self, department, courseId, section):
        """Add a section Event to the course; return False if course not found."""
        node = self._find_node(department, courseId)
        if node is None:
            return False
        node.sections.append(section)
        return True

    # ---------- traversals (string) ----------

    def _in_order(self, node):
        if node is None:
            return ""
        return self._in_order(node.left) + str(node) + self._in_order(node.right)

    def _pre_order(self, node):
        if node is None:
            return ""
        return str(node) + self._pre_order(node.left) + self._pre_order(node.right)

    def _post_order(self, node):
        if node is None:
            return ""
        return self._post_order(node.left) + self._post_order(node.right) + str(node)

    def inOrder(self):
        """Return info for all courses using in-order traversal."""
        if self.root is None:
            return ""
        return self._in_order(self.root)

    def preOrder(self):
        """Return info for all courses using pre-order traversal."""
        if self.root is None:
            return ""
        return self._pre_order(self.root)

    def postOrder(self):
        """Return info for all courses using post-order traversal."""
        if self.root is None:
            return ""
        return self._post_order(self.root)

    # ---------- other operations ----------

    def getAttendableSections(self, department, courseId, availableDay, availableTime):
        """
        For a given course (department, courseId), find all sections whose:

          - sec.day == availableDay
          - sec.time[0] >= availableTime[0]
          - sec.time[1] <= availableTime[1]

        Return a string joining all such sections (each via str(sec)),
        separated by '\n'. If there are no such sections or course doesn't
        exist, return the empty string "".
        """
        node = self._find_node(department, courseId)
        if node is None:
            return ""

        start_avail, end_avail = availableTime
        result_lines = []
        for sec in node.sections:
            if sec.day != availableDay:
                continue
            start, end = sec.time
            if start >= start_avail and end <= end_avail:
                result_lines.append(str(sec))

        if not result_lines:
            return ""
        # joined by single newlines, no extra newline at end
        return "\n".join(result_lines)

    def countCoursesByDepartment(self):
        """Return dictionary mapping department code to number of courses."""
        counts = {}

        def visit(node):
            if node is None:
                return
            visit(node.left)
            counts[node.department] = counts.get(node.department, 0) + 1
            visit(node.right)

        visit(self.root)
        return counts

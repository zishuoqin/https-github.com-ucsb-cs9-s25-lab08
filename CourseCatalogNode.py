# CourseCatalogNode.py

from Event import Event


class CourseCatalogNode:
    """Node in the course catalog BST, representing a single course."""

    def __init__(self, department, courseId, courseName, lecture, sections):
        # Keys
        self.department = department.upper()
        self.courseId = courseId
        self.courseName = courseName.upper()

        # Events
        self.lecture = lecture          # Event
        self.sections = list(sections)  # list[Event]

        # BST links
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self):
        """
        Returns a multi-line string describing this course.

        Format example:
        CMPSC 9: INTERMEDIATE PYTHON
         * Lecture: TR 15:30 - 16:45, TD-W 1701
         + Section: W 14:00 - 14:50, NORTH HALL 1109
         ...

        Note: each line ends with a '\n'.
        """
        lines = []
        # header
        lines.append(f"{self.department} {self.courseId}: {self.courseName}\n")
        # lecture
        lines.append(f" * Lecture: {self.lecture}\n")
        # sections
        for sec in self.sections:
            lines.append(f" + Section: {sec}\n")
        return "".join(lines)

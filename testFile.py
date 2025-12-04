# testFile.py
# Strong but compatible tests for Event, CourseCatalogNode, CourseCatalog.

import pytest
from Event import Event
from CourseCatalogNode import CourseCatalogNode
from CourseCatalog import CourseCatalog


# ---------- Event tests ----------

def test_event_basic_eq_and_str():
    e1 = Event("TR", (1530, 1645), "td-w 1701")
    e2 = Event("TR", (1530, 1645), "TD-W 1701")
    e3 = Event("TR", (1530, 1645), "td-w 1702")
    e4 = Event("TR", (1500, 1600), "td-w 1701")

    # equality checks relevant fields
    assert e1 == e2          # same everything except location case
    assert e1 != e3          # different location
    assert e1 != e4          # different time

    # str format
    assert str(e1) == "TR 15:30 - 16:45, TD-W 1701"


def test_event_location_and_time_stored():
    e = Event("MWF", (800, 950), "bren 1414")
    assert e.day == "MWF"
    assert e.time == (800, 950)
    # location stored uppercase
    assert e.location == "BREN 1414"


# ---------- CourseCatalogNode tests ----------

def test_node_init_and_uppercase_and_links():
    lecture = Event("TR", (1000, 1050), "td-w 1701")
    s1 = Event("W", (1400, 1450), "north hall 1109")
    sections = [s1]

    node = CourseCatalogNode("cmpsc", 9, "intermediate python", lecture, sections)

    # uppercase fields
    assert node.department == "CMPSC"
    assert node.courseId == 9
    assert node.courseName == "INTERMEDIATE PYTHON"

    # lecture / sections stored
    assert node.lecture is lecture
    assert len(node.sections) == 1

    # tree links start None
    assert node.parent is None
    assert node.left is None
    assert node.right is None


def test_node_str_exact_with_and_without_sections():
    lecture = Event("TR", (1530, 1645), "td-w 1701")
    # with sections
    s1 = Event("W", (1400, 1450), "north hall 1109")
    s2 = Event("W", (1500, 1550), "north hall 1109")
    node = CourseCatalogNode("cmpsc", 9, "intermediate python", lecture, [s1, s2])

    expected = (
        "CMPSC 9: INTERMEDIATE PYTHON\n"
        " * Lecture: TR 15:30 - 16:45, TD-W 1701\n"
        " + Section: W 14:00 - 14:50, NORTH HALL 1109\n"
        " + Section: W 15:00 - 15:50, NORTH HALL 1109\n"
    )
    assert str(node) == expected

    # without sections
    node2 = CourseCatalogNode("pstat", 131, "intro to probability", lecture, [])
    expected2 = (
        "PSTAT 131: INTRO TO PROBABILITY\n"
        " * Lecture: TR 15:30 - 16:45, TD-W 1701\n"
    )
    assert str(node2) == expected2


# ---------- CourseCatalog tests ----------

def _headers_in_output(s):
    """Helper: extract header lines 'DEPT ID: NAME' from traversal output."""
    return [line for line in s.splitlines() if ": " in line and "* Lecture" not in line]


def test_catalog_add_and_traversals_order():
    cc = CourseCatalog()
    lec = Event("TR", (1000, 1050), "td-w 1701")

    # build tree with mixed departments / ids
    assert cc.addCourse("cmpsc", 9, "a", lec, []) is True
    assert cc.addCourse("cmpsc", 270, "b", lec, []) is True
    assert cc.addCourse("cmpsc", 8, "c", lec, []) is True
    assert cc.addCourse("pstat", 131, "d", lec, []) is True
    assert cc.addCourse("art", 10, "e", lec, []) is True

    # duplicate (same dept+id) must fail
    assert cc.addCourse("CMPSC", 9, "dup", lec, []) is False

    # in-order: sorted lexicographically by (dept, id)
    in_order = cc.inOrder()
    headers_in = _headers_in_output(in_order)
    assert headers_in == [
        "ART 10: E",
        "CMPSC 8: C",
        "CMPSC 9: A",
        "CMPSC 270: B",
        "PSTAT 131: D",
    ]

    # pre-order: root first (first inserted)
    pre = cc.preOrder()
    headers_pre = _headers_in_output(pre)
    assert headers_pre[0] == "CMPSC 9: A"

    # post-order: root last
    post = cc.postOrder()
    headers_post = _headers_in_output(post)
    assert headers_post[-1] == "CMPSC 9: A"

    # empty tree traversals
    empty = CourseCatalog()
    assert empty.inOrder() == ""
    assert empty.preOrder() == ""
    assert empty.postOrder() == ""


def test_catalog_addSection_and_getAttendableSections_cases():
    cc = CourseCatalog()

    lecture = Event("TR", (1530, 1645), "td-w 1701")
    w1 = Event("W", (1400, 1450), "north hall 1109")
    w2 = Event("W", (1500, 1550), "north hall 1109")
    w3 = Event("W", (1600, 1650), "north hall 1109")
    w4 = Event("W", (1700, 1750), "girvetz hall 1112")
    f1 = Event("F", (0, 2359), "fluent-python-in-one-day hall 101")

    # course with 4 W sections
    assert cc.addCourse("cmpsc", 9, "intermediate python", lecture, [w1, w2, w3, w4]) is True

    # add Friday section via addSection (case-insensitive dept)
    assert cc.addSection("CMPSC", 9, f1) is True

    # addSection to non-existing course -> False
    assert cc.addSection("pstat", 131, w1) is False

    # 1) window W 15:00-17:00 -> only w2 & w3
    out1 = cc.getAttendableSections("cmpsc", 9, "W", (1500, 1700))
    lines1 = out1.splitlines() if out1 else []
    assert "W 15:00 - 15:50, NORTH HALL 1109" in lines1
    assert "W 16:00 - 16:50, NORTH HALL 1109" in lines1
    assert "W 14:00 - 14:50, NORTH HALL 1109" not in lines1
    assert "W 17:00 - 17:50, GIRVETZ HALL 1112" not in lines1
    assert "F 00:00 - 23:59, FLUENT-PYTHON-IN-ONE-DAY HALL 101" not in lines1

    # 2) wide window W 14:00-18:00 -> all four W sections
    out2 = cc.getAttendableSections("cmpsc", 9, "W", (1400, 1800))
    lines2 = out2.splitlines() if out2 else []
    for expected in [
        "W 14:00 - 14:50, NORTH HALL 1109",
        "W 15:00 - 15:50, NORTH HALL 1109",
        "W 16:00 - 16:50, NORTH HALL 1109",
        "W 17:00 - 17:50, GIRVETZ HALL 1112",
    ]:
        assert expected in lines2

    # 3) boundary equal to section times (closed interval)
    w_full = Event("W", (1500, 1700), "extra room 100")
    assert cc.addSection("cmpsc", 9, w_full) is True
    out3 = cc.getAttendableSections("cmpsc", 9, "W", (1500, 1700))
    lines3 = out3.splitlines() if out3 else []
    assert "W 15:00 - 17:00, EXTRA ROOM 100" in lines3

    # 4) too narrow window -> empty
    assert cc.getAttendableSections("cmpsc", 9, "W", (1510, 1600)) == ""

    # 5) wrong day -> empty
    assert cc.getAttendableSections("cmpsc", 9, "M", (0, 2359)) == ""

    # 6) course not exist -> empty
    assert cc.getAttendableSections("pstat", 199, "W", (0, 2359)) == ""

    # 7) existing course but no sections
    lec2 = Event("TR", (1300, 1350), "arts 2628")
    assert cc.addCourse("art", 10, "intro to painting", lec2, []) is True
    assert cc.getAttendableSections("art", 10, "TR", (0, 2359)) == ""


def test_catalog_countCoursesByDepartment_empty_and_multiple():
    empty = CourseCatalog()
    assert empty.countCoursesByDepartment() == {}

    cc = CourseCatalog()
    lec = Event("TR", (900, 950), "td-w 1701")
    cc.addCourse("cmpsc", 8, "x", lec, [])
    cc.addCourse("cmpsc", 9, "y", lec, [])
    cc.addCourse("pstat", 131, "z", lec, [])
    cc.addCourse("art", 10, "w", lec, [])

    counts = cc.countCoursesByDepartment()
    assert counts == {"ART": 1, "CMPSC": 2, "PSTAT": 1}

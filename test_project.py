from project import convertEndTag, convertLine, get_en_tag
import pytest


def test_convertEndTag(): 
    line = "<ن مقال>"
    convertEndTag(line) == "</p>"
    line = "<نهاية عنوان1"
    convertEndTag(line) == "</h1>"


def test_get_en_tag():
    assert get_en_tag("مقال ") == "p"
    assert get_en_tag("عنوان1 ") == "h1"
    assert get_en_tag("ليس موجود") == None


def test_convertLine():
    line = " <عنوان1>الحمد لله<ن عنوان1>".strip()
    convertLine(line) == "<h1 >الحمد لله</h1>".strip()


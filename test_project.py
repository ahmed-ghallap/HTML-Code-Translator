import pytest
from project import convert, get_en_tag, get_en_attributes, add_tag, add_attribute


def test_add_attribute():
    pass
    # newArAttribute = "ركز"
    # newEnAttribute = "autofocus"
    # add_attribute(en=newEnAttribute, ar=newArAttribute)
    # assert get_en_attributes(newArAttribute) == newEnAttribute


def test_add_tag():
    pass
    # newArTag = "استمارة"
    # newEnTag = "form"
    # add_tag(en=newEnTag, ar=newArTag)
    # assert get_en_tag(newArTag) == newEnTag

    # newArTag = "رائس"
    # newEnTag = "head"
    # add_tag(en=newEnTag, ar=newArTag)
    # assert get_en_tag(newArTag) == newEnTag

    # newArTag = "جسم"
    # newEnTag = "body"
    # add_tag(en=newEnTag, ar=newArTag)
    # assert get_en_tag(newArTag) == newEnTag

    # newArTag = "ذيل"
    # newEnTag = "footer"
    # add_tag(en=newEnTag, ar=newArTag)
    # assert get_en_tag(newArTag) == newEnTag


def test_get_en_tag():
    assert get_en_tag("مقال") == "p"
    assert get_en_tag("عنوان1") == "h1"
    assert get_en_tag("عنوان2") == "h2"
    with pytest.raises(ValueError):
        get_en_tag("عنوان3")


def test_get_en_attributes():
    assert get_en_attributes("لاتكمل").strip() == "noComplete"
    assert get_en_attributes("اكمل").strip() == "complete"
    assert get_en_attributes("فئه").strip() == "class"
    assert get_en_attributes("رابط").strip() == "link"
    assert get_en_attributes("رابط اكمل لاتكمل").strip() == "link complete noComplete"
    assert (
        get_en_attributes('رابط="https://hello.com"').strip()
        == 'link="https://hello.com"'
    )
    assert (
        get_en_attributes('رابط = "https://hello.com"').strip()
        == 'link = "https://hello.com"'
    )

    assert get_en_attributes("فلفل") == "فلفل"
    assert (
        get_en_attributes('فلفل رابط="https://www.google.com"')
        == 'فلفل link="https://www.google.com"'
    )


def test_convert():
    line = "بسم الله الحمن الرحيم"
    assert convert(line).strip() == line

    line = "<بسم الله الحمن الرحيم"
    assert convert(line).strip() == line

    line = "بسم الله الحمن الرحيم>"
    assert convert(line).strip() == line

    line = "This is not a tag"
    assert convert(line).strip() == line

    line = "<مقال>"
    assert convert(line).strip() == "<p >"

    line = "<" + 'مقال رابط="https://www.google.com"' + ">"
    assert convert(line).strip() == '<p link="https://www.google.com">'

    line = "<" + "مقال لاتكمل" + ">"
    assert convert(line).strip() == "<p noComplete>"

    line = "<" + 'مقال لاتكمل رابط="https://www.facebook.com"' + ">"
    assert convert(line).strip() == '<p noComplete link="https://www.facebook.com">'

    line += "سبحان الله" + "<" + "عنوان1" + ">"
    assert (
        convert(line).strip()
        == '<p noComplete link="https://www.facebook.com">' + "سبحان الله" + "<h1 >"
    )

    line += "الحمد لله" + "<ن عنوان1>"
    assert (
        convert(line).strip()
        == '<p noComplete link="https://www.facebook.com">'
        + "سبحان الله"
        + "<h1 >الحمد لله</h1>"
    )

    line += "<عنوان1>" + "الحمد لله" + "<ن عنوان1>"
    assert (
        convert(line).strip()
        == '<p noComplete link="https://www.facebook.com">'
        + "سبحان الله"
        + "<h1 >الحمد لله</h1>"
        + "<h1 >الحمد لله</h1>"
    )

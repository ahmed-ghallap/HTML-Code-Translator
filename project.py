import json
import os
import re


with open("tags.json") as file:
    TAGS = json.loads(file.read())
with open("attributes.json") as file:
    ATTRIBUTES = json.loads(file.read())

ENDS = ["ن", "نهاية"]
arabic = f"[\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd92-\ufdc7\ufe70-\ufefc\uFDF0-\uFDFD0-9]"


class Html:
    @classmethod
    def convert(cls, inputFile: str, outputFile=None) -> None:
        translate(inputFile, outputFile)

    @classmethod
    def add_tag(cls, en: str, ar: str) -> None:
        en = en.strip().lower()
        ar = ar.strip()
        en_exist = ar_booked = False
        for tag in TAGS:
            if tag["en"] == en:
                en_exist = True
            if tag["ar"] == ar:
                ar_booked = True
        for attribute in ATTRIBUTES:
            if attribute["ar"] == ar:
                ar_booked = True

        if ar_booked:
            raise ValueError(f"{ar} is already booked")
        if not en_exist:
            raise ValueError(f"{en} not found in our book")

        with open("tags.json", "w") as file:
            newTag = []
            for tag in TAGS:
                if tag["en"] == en:
                    tag["ar"] == ar
                    newTag.append({"en": en, "ar": ar})
                    continue
                newTag.append(tag)
            file.write(json.dumps(newTag))

    @classmethod
    def add_attribute(cls, en: str, ar: str) -> None:
        en = en.strip().lower()
        ar = ar.strip()
        en_exist = ar_booked = False
        for attribute in ATTRIBUTES:
            if attribute["en"] == en:
                en_exist = True
            if attribute["ar"] == ar:
                ar_booked = True

        for tag in TAGS:
            if tag["ar"] == ar:
                ar_booked = True

        if ar_booked:
            raise ValueError(f"{ar} is already booked")
        if not en_exist:
            raise ValueError(f"{en} not found in our book")

        with open("attributes.json", "w") as file:
            newAttribute = []
            for attribute in ATTRIBUTES:
                if attribute["en"] == en:
                    attribute["ar"] == ar
                    newAttribute.append({"en": en, "ar": ar})
                    continue
                newAttribute.append(attribute)
            file.write(json.dumps(newAttribute))


def main():
    file = Html()
    file.convert("input.txt")  # input.html
    # file.convert("input2.txt", "output.html")
    # file.add_tag(en="p", ar="مقال")
    # file.add_tag(en="h2", ar="عنوان2")
    # file.add_attribute(en="class", ar="فئه")

    # Html.add_tag(en="h2", ar="عنوان2")
    # Html.add_attribute(en="id", ar="معرف")
    Html.convert("input.txt", "hello.html")
    # Html.get_json_tags()
    # Html.get_json_attributes()


def translate(infile: str, outfile: str) -> None:
    if ".txt" not in infile:
        raise ValueError(f"{infile} does not have .txt")
    if not outfile:
        outfile = infile.removesuffix(".txt") + ".html"

    raw = []
    with open(infile) as file:
        if not file.readable():
            raise ValueError(f"{infile} is not readable")
        for line in file:
            raw.append(line)

    with open(outfile, "w") as file:
        for line in raw:
            file.write(convertLine(line) + "\n")


def convertLine(line):
    line = convertEndTag(line)
    line = convertStartTag(line)
    return line


def convertStartTag(line):  # return line
    startTag = rf'<({arabic}+)( *(?: *{arabic}*)*(?:{arabic}\s?=\s?".*")*) *>'

    if matches := re.findall(startTag, line):
        # [(tag,attributes), (...)]
        for ar_tag, ar_attributes in matches:
            if ar_tag in ENDS:
                continue

            en_attributes = get_en_attributes(ar_attributes)
            en_tag = get_en_tag(ar_tag)

            if en_tag:
                line = re.sub(startTag, f"<{en_tag} {en_attributes}>", line, 1)
    return line


def get_en_attributes(ar_attributes):
    if matches := re.findall(rf" +{arabic}+", ar_attributes):
        for match in matches:
            for attribute in ATTRIBUTES:
                if attribute["ar"] == match.strip():
                    ar_attributes = ar_attributes.replace(
                        match.strip(), attribute["en"], 1
                    )
                    break
    else:
        return ""
    return ar_attributes


def get_en_tag(ar_tag):
    ar_tag = ar_tag.strip()
    for tag in TAGS:
        if tag["ar"] == ar_tag:
            return tag["en"]
    return None


def convertEndTag(line):  # return line
    end = "(?:" + "|".join(ENDS) + ")"  # ["ن", "نهاية"]

    endTag = rf"< *{end} ({arabic}+) *>"

    if matches := re.findall(endTag, line):
        for match in matches:
            for tag in TAGS:
                if tag["ar"] == match:
                    line = re.sub(endTag, r"</" + tag["en"] + ">", line)
    return line


if __name__ == "__main__":
    main()

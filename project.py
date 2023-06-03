import re
import argparse
import json

ARABIC_LETTER = r"[_\-\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd92-\ufdc7\ufe70-\ufefc\uFDF0-\uFDFD0-9]"

START_TAG = (
    rf'<({ARABIC_LETTER}+)( *(?: *{ARABIC_LETTER}*)*(?:{ARABIC_LETTER}\s?=\s?".*")*) *>'
)

ENDS = ["ن", "نهاية"]
end = "(?:" + "|".join(ENDS) + ")"
END_TAG = rf"< *{end} ({ARABIC_LETTER}+) *>"


with open("tags.json") as file:
    TAGS = json.loads(file.read())
with open("attributes.json") as file:
    ATTRIBUTES = json.loads(file.read())


def main():
    parser = argparse.ArgumentParser(
        prog="Arabic HTML translator",
        description="Translate Arabic HTML to its corresponds in English",
        epilog="Mail for help at: ahmedor759@gmail.com",
    )

    parser.add_argument(
        "-c","--convert",
        metavar="[file-name]",
        help="Convert or translate arabic text file to HTML file",
        nargs=2
        
    )

    parser.add_argument(
        "-m", "--modify",
        help="Modify the date base by updateing tags and attributes",
        action="store_true"
    )


    args = parser.parse_args()

    if args.modify:
        flag = input("for modify tags enter 't' or 'a' for attributes\n")
        if flag == 't':
            print("You can exit the program by press  control-d")
            while True:
                try:
                    en = input("en: ")
                    ar = input("ar: ")
                    try:
                        add_tag(en=en, ar=ar)
                    except ValueError:
                        print(f"{en} not in our date base or {ar} is already booked")
                except EOFError:
                    break            

        elif flag == "a":
            while True:
                try:
                    en = input("en: ")
                    ar = input("ar: ")
                    try:
                        add_attribute(en=en, ar=ar)
                    except ValueError:
                        print(f"{en} not in our date base or {ar} is already booked")
                except EOFError:
                    break
        else:
            print(f"{flag} not a or t")
            exit()
    
    if not args.convert:
        return 

    convertedCode = []
    with open(args.convert[0]) as file:
        for line in file:
            convertedCode.append(convert(line))

    with open(args.convert[1], "w") as file:
        for line in convertedCode:
            file.write(line + "\n")


def convert(line: str) -> str:
    if matches := re.findall(r"(<[^<>]+>)", line):
        for match in matches:
            if startTagAndAttributes := re.findall(START_TAG, match):
                for startTag, Attributes in startTagAndAttributes:
                    if not startTag in ENDS:
                        enTag = get_en_tag(startTag)
                        enAttributes = get_en_attributes(Attributes)
                        line = re.sub(match, f"<{enTag} {enAttributes}>", line)

            if endTag := re.findall(END_TAG, match):
                for tag in TAGS:
                    if tag["ar"] == endTag[0]:
                        line = re.sub(match, r"</" + tag["en"] + ">", line)
                        break

    return line


def get_en_tag(arTag: str) -> str:
    arTag = arTag.strip()
    for tag in TAGS:
        if tag["ar"] == arTag:
            return tag["en"]
    raise ValueError(f"{arTag} not found in data base")


def get_en_attributes(arAttributes):
    if matches := re.findall(rf" *{ARABIC_LETTER}+", arAttributes):
        for match in matches:
            for attribute in ATTRIBUTES:
                if attribute["ar"] == match.strip():
                    arAttributes = arAttributes.replace(
                        match.strip(), attribute["en"], 1
                    )
                    break
    else:
        return ""
    return arAttributes.strip()


def add_tag(en: str, ar: str) -> None:
    global TAGS
    en = en.strip().lower()
    ar = ar.strip()

    en_exist = ar_booked = False
    for tag in TAGS:
        if tag["en"] == en and tag["ar"] == ar:
            break
        if tag["en"] == en:
            en_exist = True
        if tag["ar"] == ar:
            ar_booked = True

    if ar_booked:
        raise ValueError(f"{ar} is already booked")
    if not en_exist: 
        raise ValueError(f"{en} not found in our book")

    with open("tags.json", "w") as file:
        newTags = []
        for tag in TAGS:
            if tag["en"] == en:
                tag["ar"] == ar
                newTags.append({"en": en, "ar": ar})
                continue
            newTags.append(tag)
        file.write(json.dumps(newTags))

    with open("tags.json", "r") as file:
        TAGS = json.loads(file.read())


def add_attribute(en: str, ar: str) -> None:
    global ATTRIBUTES

    en = en.strip().lower()
    ar = ar.strip()
    en_exist = ar_booked = False
    for attribute in ATTRIBUTES:
        if attribute["en"] == en:
            en_exist = True
        if attribute["ar"] == ar:
            ar_booked = True

    if ar_booked:
        print(ar)
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

    with open("attributes.json") as file:
        ATTRIBUTES = json.loads(file.read())


if __name__ == "__main__":
    main()

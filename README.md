# HTML Code Translator
#### Video Demo: [url](https://youtu.be/gI16X7aFnrw)
#### Description:

    This program translates html code written in Arabic to html code written in English.

**How to use**

- The user should write his code in a text file.
- The text file should be in the root folder with the program
- should be there the tags, attributes json files
- The output file will be in HTML
    

**Advantages**

    The user can modify the tags and attributes to what they prefers.

**The program's idea**

    is just searching for Arabic words between <  > and then compare it with the database if find match then will convert the word to English version.

**The program depends on**
- regular exprsion:

        using regula exprsion with arabic words was diffcult becase arabic is writen rtl not ltr like english

- power of json:

        Jason is used to map Arabic words and their corresponding HTML tags

- Arabic alphabet unicode:

        To avoid not recognizing the language from one device to another, Unicode is the most accurate encoding known

**The purpose of the program**

     is to facilitate writing the code for Arab beginners who face the problem of learning the English language

**The next feature of this program**

- Use python GUI:
    
         to write input file and tags, attributes

- Convert css files:

        the user can write css in a text file in arabic and convert it to english

- Use of multiple languages:

        can use the program with any other language and convert it to english

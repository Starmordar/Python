import sys
import xml.sax.saxutils as sax

def main():
    options = maxwidthv, formatv = process_options()
    if options != (None, None):
        print_table_start_html_tag()
        count = 0
        while True:
            try:
                line = input()
                if count == 0:
                    color = "lightgreen"
                elif count % 2:
                    color = "white"
                else:
                    color = "lightyellow"
                print_line(line, color, maxwidthv, formatv)
                count += 1
            except EOFError:
                break
        print_table_end_html_tag()


def print_table_start_html_tag():
    print("<table border='1'>")


def print_table_end_html_tag():
    print("</table>")


def print_line(line, color, maxwidth, formatv):
    print("<tr bgcolor='{0}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print("<td align='right'>{0:{1}}</td>".format(x, formatv))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                field = sax.escape(field)
                if len(field) <= maxwidth:
                    print("<td>{0}</td>".format(field))
                else:
                    print("<td>{0:.{1}} ...</td>".format(field, maxwidth))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:  
                quote = c
            elif quote == c:  
                quote = None
            else:
                field += c
                continue
        if quote is None and c == ",":  
            fields.append(field)
            field = ""
        else:
            field += c
    if field:
        fields.append(field) 
    return fields


def process_options():
    default_maxwidth = 100
    default_format = ".0f"
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            message = """usage:
csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html
maxwidth - необязательное целое число. Если задано, определяет
максимальное число символов для строковых полей. В противном случае
используется значение по умолчанию 100."""
            print(message)
            return None, None
        else:
            for arg in sys.argv[1:]:
                if arg.startswith("maxwidth"):
                    default_maxwidth = int(arg.split("=")[1])
                elif arg.startswith("format"):
                    default_format = arg.split("=")[1]

    return default_maxwidth, default_format


main()
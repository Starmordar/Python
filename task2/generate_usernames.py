import collections
import sys

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

User = collections.namedtuple("User",
            "username forename middlename surname id")

def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)

    return username

def get_page_header(namewidth, usernamewidth):
    header = "{0:<{nw}} {1:^6} {2:{uw}}".format(
        "Name", "ID", "Username", nw=namewidth, uw=usernamewidth)
    headers_spaces = "  "

    first_combined_headers = header + headers_spaces + header
    hr = "{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
        "", nw=namewidth, uw=usernamewidth)
    second_combined_headers = hr + headers_spaces + hr

    return first_combined_headers + "\n" + second_combined_headers

def get_user_data(user, namewidth, usernamewidth, ellipsis_text_length):
    tempData = ""
    if user.middlename:
        tempData = " " + user.middlename[0]

    name = "{0.surname}, {0.forename}{1}".format(user, tempData)

    return "{0:.<{nw}.{np}} ({1.id:4}) {1.username:{uw}}".format(
        name, user, nw = namewidth, uw = usernamewidth, np = namewidth - ellipsis_text_length)

def print_users(users):
    namewidth = 17
    usernamewidth = 9
    ellipsis_text_length = 0
    max_page_length = 64

    page_header = get_page_header(namewidth, usernamewidth)
    sorted_users = sorted(users)

    for i, (lcol, rcol) in enumerate(zip(sorted_users[::2], sorted_users[1::2])):
        if i % max_page_length == 0:
            print("\f" + page_header)

        record = "{}{}".format("  ", get_user_data(users[rcol], namewidth, usernamewidth, ellipsis_text_length)) if rcol is not None else ""
        print(get_user_data(users[lcol], namewidth, usernamewidth, ellipsis_text_length) + record)

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {}
    for filename in sys.argv[1:]:
        with open(filename, encoding="utf8") as file:
            for line in file:
                line = line.rstrip()
                if line:
                    user = process_line(line, usernames)
                    users[(user.surname.lower(), user.forename.lower(),
                            user.id)] = user
    print_users(users)

main()
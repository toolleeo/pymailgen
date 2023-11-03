import argparse
import csv
import sys
import re

sender_script_filename = 'sendall.sh'
ssmtp_line_template = 'ssmtp {Address} < {EmailFName}'
send_line_template = ssmtp_line_template

def init_argparser():
    """Initialize the command line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('body', action="store", type=str,
                        help="Text file containing the body of the message")
    parser.add_argument('datafile', action="store", type=str,
                        help="File containing the variable data to fill the emails")
    parser.add_argument('--ssmtp', '-s', metavar='HEADER',
                        help='Sets ssmtp to send the emails; requires the header file containing the sending information.')
    return parser


def read_data_file(data_file, delimiter=',', quotechar='"'):
    """Loads the data used to fill the emails."""
    data = []
    with open(data_file, 'r') as f:
        lines = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for l in lines:
            data.append(l)
    return data


def is_valid_address(email_address):
    """Check the validity of an email address."""
    if re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
        return True
    else:
        return False


def process(email_text, data, send_line_template):
    """Generates an email file for each item in the input data."""
    n = len(str(len(data)))
    email_filename_template = 'email_{{:0{}d}}.txt'.format(n)
    # gets an empty sender script file
    with open(sender_script_filename, 'w') as f:
        pass
    i = 0
    for j, item in enumerate(data):
        if 'Blacklist' in item:
            if item['Blacklist'] != '':
                continue
        email = email_text.format(**item)
        email_filename = email_filename_template.format(i)
        addr = item['Email']
        if not is_valid_address(addr):
            print('Invalid email address "{}" at line {}'.format(addr, j + 1))
            continue
        with open(email_filename, 'w') as f:
            f.write(email)
        fields = {'Address': addr, 'EmailFName': email_filename}
        send_line = send_line_template.format(**fields)
        with open(sender_script_filename, 'a') as f:
            f.write(send_line + '\n')
            f.write(f'echo "[$(date +\"%Y-%m-%d %T.%3N\")] Email #{i} to {addr}" | tee -a auto_mailer.log\n')
        i += 1


def check_data_file(data):
    """Perform some checkings on the input data file.

    Returns None if everything is alright. Otherwise an error string.
    The error string has a placeholder for the filename."""
    if len(data) < 1:
        return '{}: data file must contain at least one row.'
    if 'Email' not in data[0]:
        return '{}: data file must contain the "Email" column (case-sensitive).'
    return None


def main():
    parser = init_argparser()
    args = parser.parse_args()

    data = read_data_file(args.datafile)
    err_string = check_data_file(data)
    if err_string is not None:
        print(err_string.format(args.datafile))
        return

    with open(args.body, 'r') as f:
        body = f.read()
    if args.ssmtp is not None:
        with open(args.ssmtp, 'r') as f:
            header = f.read()
        email_text = header + '\n' + body
        send_line_template = 'ssmtp -t < {EmailFName}'
    else:
        email_text = body
    process(email_text, data, send_line_template)


if __name__ == "__main__":
    main()

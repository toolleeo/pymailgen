import csv
import sys
import argparse

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
    data = []
    with open(data_file, 'r') as f:
        lines = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for l in lines:
            data.append(l)
    return data


def process(email_text, data):
    # prints an email for each template
    n = len(str(len(data)))
    #print(n)
    email_filename_template = 'email_{{:0{}d}}.txt'.format(n)
    #print(email_filename_format)
    with open(sender_script_filename, 'w') as f:
        pass
    i = 0
    for item in data:
        email = email_text.format(**item)
        #print(email)
        email_filename = email_filename_template.format(i)
        #print(email_filename)
        addr = item['Email']
        with open(email_filename, 'w') as f:
            f.write(email)
        fields = {'Address': addr, 'EmailFName': email_filename}
        #send_line = send_line_template.format(address, email_filename)
        send_line = send_line_template.format(**fields)
        with open(sender_script_filename, 'a') as f:
            f.write('echo "Sending #{} to {}"'.format(i, addr) + '\n')
            f.write(send_line + '\n')
        i += 1


def check_data(data):
    if len(data) < 1:
        print('Data file must contain at least one row.')
        sys.exit(1)
    if 'Email' not in data[0]:
        print('Data file must contain the "Email" colummn (case-sensitive).')
        sys.exit(1)


def main():
    parser = init_argparser()
    args = parser.parse_args()

    data = read_data_file(args.datafile)
    check_data(data)
    #print(data)

    with open(args.body, 'r') as f:
        body = f.read()
    #print(body)
    if args.ssmtp is not None:
        with open(args.ssmtp, 'r') as f:
            header = f.read()
        email_text = header + '\n' + body
    else:
        email_text = body
    #print(email_text)
    process(email_text, data)


if __name__ == "__main__":
    main()

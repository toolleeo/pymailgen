# pymailgen

Starting from the content of a CSV file and a template text file, `pymailgen` generates a list of emails to be sent out using a command-line SMTP client.

`pymailgen` does not send the emails itself, but it relies on external command-line tools to do it.
`pymailgen` generates a shell script called `sendall.sh` that contains the list of commands to send out the emails using a command line STMP client.

This two-stage procedure has at least two advantages:

1. you can inspect the emails before sending them out;
2. in case of any issue in the sending, you have a log of what happened, and you can send the failed emails by just manually editing the `sendall.sh` script to keep the necessary corresponding commands.

At the moment, the only supported SMTP client is `ssmtp`.
Some useful info to configure `ssmtp` for being used with Gmail are reported [in this blog](https://blog.edmdesigner.com/send-email-from-linux-command-line/).

The logic of `pymailgen` is super simple.
Therefore, it is easy to hack and customize in case a more complex logic is required to fill the template.

# How it works

The elements required to generate the emails are:

* the body of the email: a plain text file template with placeholders;
* the header of the email: a plain text file with standard email header format;
* the list of recipients: a CSV file with as many optional fields as needed.

The body and the header of the email can contain placeholders in the form of `{Field}`.
For each email, `pymailgen` replaces the placeholder with the value in the column `Field` in a CSV file containing the necessary information.
Association between field and placeholder is case-sensitive.

Each individual generated email is stored in a file named `email_X.txt`, where `X` is an incremental number.

Once all the necessary data are in place, run the following command to generate the emails:

```
pymailgen body.txt contacts.csv --ssmtp header.txt
```

If the SMTP client is properly configured, the emails will be sent out by running

```
bash sendall.sh
```

## Blacklisting

If the input CSV file contains a column named `Blacklist` (case-sensitive), every row with any non-empty content in that column will be skipped during the generation of the set of emails.

# auto_mailer

`auto_mailer` generates a list of emails to be sent out using a command-line SMTP client.

The main components are:

* the body of the email
* the header of the email
* the list of recipients with as many optional fields as needed

The body and the header of the email can contain placeholders in the form of `{Field}`. For each email, `auto_mailer` replaces the placeholder with the value in the column `Field`. Association between field and placeholder is case-sensitive.

`auto_mailer` does not send the emails itself. It relies on external command-line tools to do it. `auto_mailer` generates a shell script called `sendall.sh` that contains the list of commands to send out the emails using a command line STMP client.

At the moment, the only supported SMTP client is `ssmtp`.
Some useful info to configure `ssmtp` for being used with Gmail are reported [in this blog](https://blog.edmdesigner.com/send-email-from-linux-command-line/).

Once all the necessary data are in place, run the following command to generate the emails:

```
python3 auto_mailer.py body.txt contacts.csv --ssmtp header.txt
```

If the SMTP cliet is properly configured, the emails can be sent by running

```
sh sendall.sh
```

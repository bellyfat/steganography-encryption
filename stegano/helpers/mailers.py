from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..log import logger
from . import loadconf
import smtplib
import threading

conf = loadconf()


def send_mail(to, subj, content, html=True):
    frm = conf.MAIL_DEFAULT_SENDER
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = frm
    msg['To'] = to

    # Prepare actual message
    msg.attach(MIMEText(content, 'html'))
    try:
        server = smtplib.SMTP(conf.MAIL_SERVER, conf.MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(conf.MAIL_USERNAME, conf.MAIL_PASSWORD)
        server.sendmail(frm, to, msg.as_string())
        server.close()
        logger.debug('Successfully sent the mail')
        return 'Successfully sent the mail'
    except Exception as e:
        logger.exception('Failed mail %s' % (e))
        return "Failed to send mail, %s " % e


def send_signup_mail(frm, to):
    subj = 'You have a Stegano Invite!'
    content = "<html>"\
        "<head></head>"\
        "<body>Hi,\n"\
        "<p>You've received a stegano message from %s."\
        " Please signup at <a href='%s/signup' target='_blank'>"\
        "Stegano Project</a> to view your message.</p>"\
        "<br>Thanks,<br>"\
        "<i>Team Stegano</i>"\
        "</body>"\
        "</html>" % (frm, conf.HOST_DOMAIN)
    thread = threading.Thread(
        target=send_mail, args=(to, subj, content), daemon=True)
    thread.start()

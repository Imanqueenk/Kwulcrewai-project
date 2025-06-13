def summarize_emails(user, app_password):
    try:
        import imaplib
        import email
        from email.header import decode_header

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(user, app_password)
        imap.select("inbox")

        status, messages = imap.search(None, 'UNSEEN')
        email_ids = messages[0].split()[-5:]

        email_summaries = []

        for eid in email_ids:
            res, msg = imap.fetch(eid, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    email_summaries.append(f"• {subject}")

        imap.logout()

        return "📬 Unread Email Summary:\n" + "\n".join(email_summaries) if email_summaries else "No new unread emails."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
import tkinter as tk
import imaplib
import email
from email.header import decode_header

# Function to summarize emails
def summarize_emails(user, app_password):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(user, app_password)
        imap.select("inbox")

        status, messages = imap.search(None, 'UNSEEN')
        email_ids = messages[0].split()[-10:]

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

# Function to update the GUI with summary
def update_summary():
    user = email_entry.get()
    app_password = password_entry.get()
    summary = summarize_emails(user, app_password)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, summary)

# GUI setup
root = tk.Tk()
root.title("📧 Email Summarizer")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Gmail:").pack()
email_entry = tk.Entry(frame, width=40)
email_entry.pack()

tk.Label(frame, text="App Password:").pack()
password_entry = tk.Entry(frame, width=60, show="*")
password_entry.pack()

summary_button = tk.Button(frame, text="Get Summary", command=update_summary)
summary_button.pack(pady=10)

result_box = tk.Text(frame, width=80, height=30)
result_box.pack()

# Start the app
if __name__ == "__main__":
    root.mainloop()
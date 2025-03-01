import win32com.client as win32


def email(address: str, subject: str, content: str) -> None:
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = address
    mail.Subject = subject
    mail.Body = content



    mail.Send()
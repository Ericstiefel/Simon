
import win32com.client as win32

def email(address: str, subject: str, body: str):
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = address
    mail.Subject = subject
    mail.Body = body

    mail.Send()
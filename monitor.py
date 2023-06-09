from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import smtplib
import file_types

source_code_extensions = file_types.source_code_extensions
media_extensions = file_types.media_extensions
doc_extensions = file_types.doc_extensions

receiver = 'shrutipriyain@gmail.com'
observed_folder = 'C:/Users/Shruti Priya/Desktop'

def send_mail(receiver, subject, body):
    emailAddress = os.environ.get('GMAIL_UNAME')
    emailPassword = os.environ.get('GMAIL_PASS') 

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo() 
        smtp.starttls()
        smtp.ehlo()

        smtp.login(emailAddress, emailPassword)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(emailAddress,receiver,msg) # smtp.sendmail(SENDER, RECEIVER, EMAIL_MSG)

class Handler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            folder_name = os.path.basename(event.src_path)
            subject = 'NEW FOLDER CREATED'
            body = f'New folder named {folder_name} was created'
            send_mail(receiver, subject, body)
        
        else:
            file_name = os.path.basename(event.src_path)
            file_extension = os.path.splitext(file_name)[1]
            file_size = os.path.getsize(event.src_path)

            if file_extension in doc_extensions:
                # send mail as safe
                subject = 'NEW DOCUEMENT CREATED'
                body = f'New document named {file_name}{file_extension} of size {file_size} was created'
                send_mail(receiver, subject, body)

            elif file_extension in media_extensions:
                # send mail as moderate
                subject = 'ATTENTION ! NEW MEDIA FILE CREATED'
                body = f'New media file named {file_name}{file_extension} of size {file_size} was created'
                send_mail(receiver, subject, body)

            else:
                # send mail as critical
                subject = 'URGENT! ACTION REQUIRED'
                body = f'New code file named {file_name}{file_extension} of size {file_size} was created'
                send_mail(receiver, subject, body)

    def on_modified(self, event):

        if event.is_directory:
            # send mail as directory modified
            folder_name = os.path.basename(event.src_path)
            subject = 'FOLDER MODIFIED'
            body = f'A folder named {folder_name} was modified'
            send_mail(receiver, subject, body)
            
        else:
            file_name = os.path.basename(event.src_path)
            file_extension = os.path.splitext(file_name)[1]
            file_size = os.path.getsize(event.src_path)
            
            if file_extension in doc_extensions:
                # send mail as safe
                subject = 'DOCUEMENT MODIFIED'
                body = f'A document named {file_name}{file_extension} of size {file_size} was modified'
                send_mail(receiver, subject, body)
                
            elif file_extension in media_extensions:
                # send mail as moderate
                subject = 'ATTENTION: MEDIA MODIFIED'
                body = f'Media named {file_name}{file_extension} of size {file_size} was modified'
                send_mail(receiver, subject, body)
                
            else:
                # send mail as critical
                subject = 'CRITICAL! ACTION REQUIRED'
                body = f'A source code file named {file_name}{file_extension} of size {file_size} was modified'
                send_mail(receiver, subject, body)
    

observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, observed_folder, recursive=True)
observer.start()

try:
        while True:
            time.sleep(1)
finally:
    observer.stop()
    observer.join()
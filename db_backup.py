import os
import ftplib


# database backup for local server

db_pass = os.environ.get('DB_PASS')
database ='CBDNS'

os.system(f'mysqldump -u root -p{db_pass} -h localhost {database} > database_backup.sql')


# database backup on remote server using FTP


ip_addr ='ftp.experienceaudition.com'
user_name ='shrutipriya'
user_pass ='@ShrutiPriya1'
session = ftplib.FTP(ip_addr,user_name, user_pass)
file = open('database_backup.sql', 'rb')
session.storbinary('STOR database_backup.sql', file)
file.close()
session.quit()

print("Backup successfully taken")

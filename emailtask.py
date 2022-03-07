import imaplib
import email
import configparser
import logging
from sqlite3 import Date

config = configparser.ConfigParser()
config.read("configuration.ini")

log_level= config.get("level","level1")
#log_file= config.get("level","logfile")

logging.basicConfig(filename='/home/vineet/Music/example.log', encoding='utf-8', level=log_level)

#logging.debug('This message should go to the log file')

data_file= config.get("data", "datafile")
z = open(data_file, 'w') #create a file to write

host = config.get("login", "host")
user = config.get("login", "user")
password = config.get("login","password")
directory= config.get("login","directory")


#user= str(input('Enter Your Email to login : '))
#password= getpass.getpass('Password : ')
mail = imaplib.IMAP4_SSL(host)
mail.login(user,password)
mail.select(directory)


#DIR = os.path.abspath(os.path.dirname(__file__))
#LOGS = [
#        os.path.join(DIR, 'logs', 'error.log'),
#        os.path.join(DIR, 'logs', 'access.log')
#]

def get_inbox(to_user,from_user,subject,nosubject,date1,date2):
    s= 'SUBJECT'
    ns= 'NOT SUBJECT'
    #s= "( FROM " + from_user + " TO " + to_user + " SUBJECT " + subject + " NOT SUBJECT " + nosubject + " ON " + date + " )"
    #print(s)
    _, search_data = mail.search(None, s, subject, ns , nosubject , 'FROM', from_user, 'TO', to_user, 'SINCE', date1 , 'BEFORE' , date2)
    #_, search_data = mail.search(None, '(FROM "'(from_user)'" TO "'(to_user)'" SUBJECT "'(subject)'" NOT SUBJECT "'(nosubject)'" ON "'(date)'")')
   # _, search_data = mail.search(None, '(FROM "ranjank.jha@fosteringlinux.com" TO "allemp@fosteringlinux.com" SUBJECT "Error" NOT SUBJECT "RE: Error" ON "22-Feb-2022")')
    for num in search_data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject' , 'to', 'from', 'date']:
            print("{} --> {}".format(header, email_message[header])) #to print on console
            print("{} --> {}".format(header, email_message[header]),file=z) #to print on file
            print("************************************************\n", file=z)
    Tot = len(search_data[0].split())
    print ( "Total number of questions asked = ", Tot, file=z)


    #get_inbox(to,from_user,subject,nosubject,date)
if __name__ == "__main__":
    to_user = config.get("search", "to")
    from_user = config.get("search", "from_user")
    subject = config.get("search", "subject")
    nosubject = config.get("search", "nosubject")
    date1 = config.get("search", "date1")
    date2 = config.get("search", "date2")
    get_inbox(to_user,from_user,subject,nosubject,date1,date2)
    

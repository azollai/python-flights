import smtplib
fromMy = 'zozo.mailtest@yahoo.com' # fun-fact: "from" is a keyword in python, you can't use it as variable.. did anyone check if this code even works?
to  = 'andrszollai@gmail.com'
subj='just$for$test'
date='2/1/2010'
message_text='Hello Or any thing you want to send'

msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )
  
username = str('zozo.mailtest@yahoo.com')  
password = str('just$for$test')  
  
try :
    server = smtplib.SMTP("smtp.mail.yahoo.com",587)
    server.ehlo()
    server.starttls() 
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromMy, to,msg)
    server.quit()    
    print('ok the email has sent')
except Exception as e:
    print(e)
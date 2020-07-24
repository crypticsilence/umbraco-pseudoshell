Source: https://www.exploit-db.com/exploits/46153

- Exploit Title: Umbraco CMS - Remote Code Execution by authenticated administrators
- Dork: N/A
- Date: 2019-01-13
- Exploit Author: Gregory DRAPERI & Hugo BOUTINON
- Modified by: crypticsilence 2020-04-11
- Vendor Homepage: http://www.umbraco.com/
- Software Link: https://our.umbraco.com/download/releases
- Version: 7.12.4
- Category: Webapps
- Tested on: Windows IIS
- CVE: N/A

Modified original code to create a pseudoshell in cmd and powershell.

Found that these are not valid in XML elements:

```
"   &quot;
'   &apos;
<   &lt;
>   &gt;
&   &amp;
```

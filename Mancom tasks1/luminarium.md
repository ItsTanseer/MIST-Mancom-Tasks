#PIPING- Split piping stderr and stdout

Now, let's put your knowledge together. You must master the ultimate piping task: redirect stdout to one program and stderr to another.

The challenge here, of course, is that the | operator links the stdout of the left command with the stdin of the right command. Of course, you've used 2>&1 to redirect stderr into stdout and, thus, pipe stderr over, but this then mixes stderr and stdout. How to keep it unmixed?

You will need to combine your knowledge of >(), 2>, and |. How to do it is a task I'll leave to you.

In this challenge, you have:

/challenge/hack: this produces data on stdout and stderr
/challenge/the: you must redirect hack's stderr to this program
/challenge/planet: you must redirect hack's stdout to this program

###Solution

/challenge/hack 2> >(/challenge/the) | /challenge/planet 

Using process substitution, 
>(/challenge/the) is the process substitution. The shell runs /challenge/the and creates a special temporary file such as /dev/fd/63 that serves as the input pipe for /challenge/the.

#File Globbing
###Multiple Globs

So far, you've specified one glob at a time, but you can do more! Bash supports the expansion of multiple globs in a single word. For example:

hacker@dojo:~$ cat /*fl*
pwn.college{YEAH}
hacker@dojo:~$
What happens above is that the shell looks for all files in / that start with anything (including nothing), then have an f and an l, and end in anything (including ag, which makes flag).

Now you try it. We put a few happy, but diversely-named files in /challenge/files. Go cd there and run /challenge/run, providing a single argument: a short (3 characters or less) globbed word with two * globs in it that covers every word that contains the letter p.

Terminal:

hacker@globbing~multiple-globs:~$ /challenge/run 
Error: please run with a working directory of /challenge/files!
hacker@globbing~multiple-globs:~$ cd /challenge/files *p*
bash: cd: too many arguments
hacker@globbing~multiple-globs:~$ cd /cha*
hacker@globbing~multiple-globs:/challenge$ cd /fi*
bash: cd: /fi*: No such file or directory
hacker@globbing~multiple-globs:/challenge$ cd files
hacker@globbing~multiple-globs:/challenge/files$ /challenge/run *p*
You got it! Here is your flag!
pwn.college{8A77cViypBRG-yXoVT31L-a-abs.0lM3kjNxwCOxIDOzEzW}
hacker@globbing~multiple-globs:/challenge/files$ 

#Snooping on configurations
Even without making mistakes, users might inadvertently leave themselves at risk. For example, many files in a typical user's home directory are world-readable by default, despite frequently being used to store sensitive information. Believe it or not, your .bashrc is world-readable unless you explicitly change it!

hacker@dojo:~$ ls -l ~/.bashrc
-rw-r--r-- 1 hacker hacker 148 Jun  7 05:56 /home/hacker/.bashrc
hacker@dojo:~$
You might think, "Hey, at least it's not world-writable by default"! But even world-readable, it can do damage. Since .bashrc is processed by the shell at startup, that is where people typically put initializations for any environment variables they want to customize. Most of the time, this is innocuous things like PATH, but sometimes people store API keys there for easy access. For example, in this challenge:

zardus@dojo:~$ echo "FLAG_GETTER_API_KEY=sk-XXXYYYZZZ" > ~/.bashrc
Afterwards, Zardus can easily refer to the API key. In this level, users can use a valid API key to get the flag:

zardus@dojo:~$ flag_getter --key $FLAG_GETTER_API_KEY
Correct API key! Do you want me to print the key (y/n)? y
pwn.college{HACKED}
zardus@dojo:~$
Naturally, Zardus stores his key in .bashrc. Can you steal the key and get the flag?

###Terminal
hacker@shenanigans~snooping-on-configurations:~$ cat /home/zardus/.bashrc

Last line of the output was: FLAG_GETTER_API_KEY=sk-759611930

Changing directory to hacker: hacker@shenanigans~snooping-on-configurations:~$ cd /home/hacker
hacker@shenanigans~snooping-on-configurations:~$ flag_getter --key $FLAG_GETTER_API_KEY
Incorrect API key!
hacker@shenanigans~snooping-on-configurations:~$ flag_getter --key $sk-759611930
Incorrect API key!
hacker@shenanigans~snooping-on-configurations:~$ flag_getter --key sk-759611930
Correct API key! Do you want me to print the flag (y/n)?
y
pwn.college{UVOyYbL6bPM7d6QRIttFufXmcJY.0lM0EzNxwCOxIDOzEzW}

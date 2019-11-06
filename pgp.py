#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

print("""\033[1m
██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗
██╔══██╗██╔════╝ ██╔══██╗██╔══██╗╚██╗ ██╔╝
██████╔╝██║  ███╗██████╔╝██████╔╝ ╚████╔╝ 
██╔═══╝ ██║   ██║██╔═══╝ ██╔═══╝   ╚██╔╝  
██║     ╚██████╔╝██║██╗  ██║        ██║   
╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═╝        ╚═╝   \033[0;2m
By Gecko

\033[1;91mWARNGING:\033[0;91m User input is not sanitized\nuse are your own risk.\033[0m
""")

def run(command, comm=None):
    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = process.communicate(input=comm)
    if not error:
        return output.decode('utf-8')
    else:
        raise error

def multiline(end="\n"):
    inputList = []
    inputText = None
    while inputText != end:
        inputText = input()
        inputList.append(inputText)

    return "\n".join(inputList)

def finaloutput(text):
    line_length = 65
    if text:
        print("\n\033[1;92mOUTPUT\n{}\n\033[0m{}\033[0m\033[1;92m{}\n".format("="*line_length, text,"="*line_length))
    else:
        print("\033[31;1mERROR\033[0m\n")

try:
    while True:
        print("""
\033[1;32m1.\033[0;32m Encrypt text 🔒
\033[1;31m2.\033[0;31m Decrypt text 🔑
\033[93;1m3.\033[0;93m Export key(s) 🔐
\033[36;1m4.\033[0;36m Import key(s) 📥
\033[94;1m5.\033[0;94m Exit 🚫
\033[0m""")

        choice = ""
        while choice not in ["1","2","3","4","5"]:
            choice = input("> ")

        if choice == "1":
            print("\n\033[1mText to encrypt \033[0;90m(blank line to finish)\033[0m\n" + "="*40)
            text = multiline("")
            print("\033[1mAvailable keys\033[0m")

            print(run("gpg --list-keys"), end="")
            recipient = ""
            while recipient == "":
                recipient = input("\033[32;1mRecipient Name:\033[0m ")
            print()
            command = "gpg -e -a -r {}".format(recipient)

            command_output = run(command, text.encode())
            finaloutput(command_output)

        elif choice == "2":
            print("\n\033[1mData to decrypt \033[0;90m(END PGP MESSAGE to finish)\033[0m\n" + "="*45)
            output = multiline(end="-----END PGP MESSAGE-----")
            command = "gpg -d -a"

            command_output = run(command, output.encode())
            finaloutput(command_output)
        
        elif choice == "3":
            print(run("gpg --list-keys"), end="")
            recipient = input("\033[32;1mExport Name \033[0;32m(blank for all):\033[0m ")
            print()
            command = "gpg -a --export {}".format(recipient)

            command_output = run(command)
            finaloutput(command_output)

        elif choice == "4":
            print("\n\033[1mImport Key \033[0;90m(END PGP MESSAGE to finish)\033[0m\n" + "="*40)
            text = multiline("-----END PGP PUBLIC KEY BLOCK-----")
            
            command = "gpg --import"
            run(command, text.encode())
        
        elif choice == "5":
            exit()

except KeyboardInterrupt:
    print("\n\033[31;1mStopped by user\033[0m\n")
    exit()

#!/usr/bin/env python3

import sys
import random
import string
import argparse
import os

def get_args():
   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument('--mixed_case', '-mc', type=str, help='Mixed Case?', required=False)
   parser.add_argument('--include_numbers', '-in', type=str, help='Include Numbers in Password?', required=False)
   parser.add_argument('--include_special_chars', '-is', type=str, help='Include Special Characters in Password?', required=False)
   parser.add_argument('--length', '-l', type=int, help='Length of Password', required=False)
   parser.add_argument('--name', '-n', type=str, help='Name of this password (no spaces)', required=False)
   parser.add_argument('--path', '-p', type=str, help='Path to save file', required=False)
   parser.add_argument('--save', '-s', type=str, help='Save to file?', required=False)

   args = parser.parse_args()

   #print("value: " + args.include_numbers)

   mixed_case=args.mixed_case
   include_numbers=args.include_numbers
   include_special_chars=args.include_special_chars
   length=args.length
   name=args.name
   path=args.path
   save=args.save
   filename=None


   special_chars="#$%&'()*+,/:;<=>?@[\]^`{|}~ "
   if name != None:
      if any(c in special_chars for c in name):
         name=None

   while name == None:
      # --> python2 name = input("Enter Name of password: ")
      name = input("Enter Name of password: ")
      if any(c in special_chars for c in name):
         print("--ERROR-- Name should not contain special characters")
         name = None

   while save == None:
      save = input("Save password to file [%s.pwd]? " %name)
      if save.lower() in ['y', 'yes', 'n', 'no']:
         if save.lower() in ['y', 'yes']:
            save='y'
            while path == None:
               path = input("Path to save %s.pwd? " %name)
               if not os.path.isdir(path):
                  print("--ERROR-- Please make sure %s exists first" %path)
                  path=None
         else:
            save='n'
      else:
         print("--ERROR-- Excepted answers are [y|yes|n|no] -- Try again")
         save = None
              
   if save == 'y':
      path = os.path.abspath(path)
      if path.endswith('/') and len(path) > 1:
         path=path[:-1]
      filename=os.path.join(path, name + ".pwd")

   if length == None:
      while length == None:
         length = input("Password Length: ")
         try:
            length=int(length)
            if length <= 0:
               raise ValueError
         except:
            print("--ERROR-- length must be an integer > 0, try again")
            length=None

   #######
   if mixed_case == None:
      while mixed_case == None:
         mixed_case = input("Include Mixed Case? ")
         if mixed_case.lower() in ['y', 'yes', 'n', 'no']:
            if mixed_case.lower() in ['y', 'yes']:
               mixed_case='y'
         else:
            print("--ERROR-- Excepted answers are [y|yes|n|no] -- Try again")
            mixed_case=None
    ########

   if include_numbers == None:
      while include_numbers == None:
         include_numbers = input("Include Numbers in Password? ")
         if include_numbers.lower() in ['y', 'yes', 'n', 'no']:
            if include_numbers.lower() in ['y', 'yes']:
               include_numbers='y'
         else:
            print("--ERROR-- Excepted answers are [y|yes|n|no] -- Try again")
            include_numbers=None
      
   if include_special_chars == None:
      while include_special_chars == None:
         include_special_chars = input("Include special characters in Password? ")
         if include_special_chars.lower() in ['y', 'yes', 'n', 'no']:
            if include_special_chars.lower() in ['y', 'yes']:
               include_special_chars='y'
         else:
            print("--ERROR-- Excepted answers are [y|yes|n|no] -- Try again")
            include_special_chars=None         


   char_string=string.ascii_letters

   if include_numbers == 'y':
      char_string="%s%s" %(char_string, string.digits)

   if include_special_chars == 'y':
      char_string="%s%s" %(char_string, string.punctuation)

   if mixed_case == 'y':
       s=string.ascii_letters.upper()
       char_string="%s%s" %(char_string, s)

   return length, char_string, filename

def generatePassword(length, char_string):
   result_str = ''.join(random.choice(char_string) for i in range(length))

   return result_str

def main():
   print("**************************************************")
   print("* Starting Program to generate random password")
   print("**************************************************\n")

   length, char_string, filename = get_args()

   print("\nLength of Password: %s" %(str(length)))
   if filename != None:
      print("File: %s" %filename)

   password = generatePassword(length, char_string)

   if filename != None:
      print("Save to file..")
      with open(filename, 'w') as f:
         f.write(password + '\n')

      print("\nPassword successfully saved to %s\n\n" %filename)

   print("\nProgram Completed\n")
   sys.exit(0)


if __name__ == "__main__":
   main()


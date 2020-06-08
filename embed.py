#embedding files
import os
a=input("specify cover file : ")
b=input("specify embed file : ")
print("\nPlease provide extension of output file as same as cover file \n")
c=input("specify output file name : ")
try:
	#read binary data of cover file and embed files
	in_file1=open(a,"rb").read()
	in_file2=open(b,"rb").read()
	out_file=open(c,"wb")
	#write the binary of files into new file
	out_file.write(in_file1)
	out_file.write(in_file2)
	print("\nFile is embed into file "+c)
except:
	print("\nPlease check for the filename or path of file")
	quit()
print("Have a nice day!!")
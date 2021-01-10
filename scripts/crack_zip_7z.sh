#!/usr/bin/env bash
##	make sure zip and 7z commands are present
## 	in bash,return code 0 is success and 1 is failure

#creating global array element
args=( "$@" )

#check file exists or mot
function exist {
	if [[ -s $1 && -f $1 ]]; then
		echo 0	#if file exists
	else 
		echo 1	#if file not exists
	fi
}

function getWordlist(){
	#check whether wordlist is specified or not
	index=$(($1+1))
	if [ ${#args[*]} -lt $(($index+1)) ]; then echo "Specify the wordlist file path."; exit 1; fi;
	wordlist_file=${args[$index]}
}

#help options
help(){
	echo -e "Usage: $0 <file> -w <wordlist>"
	echo -e "\nOptions"
	echo " -w   specify wordlist file path"
	echo " -h   display help option and exit"
	exit 0
}

#check whether file is specified or not
if [ ${#args[@]} -eq 0 ]
then
	echo "Usage: $0 <file> -w <wordlist>"
	exit 0
else
	index=0
	flag=1
	for i in $@; do
		if [ $i = "-h" ]; then help ;
		elif [[ $i == "-w" ]]; then getWordlist $index ; flag=0;
		fi
		index=$(($index+1))
	done
	if [ $flag -eq 1 ];then echo -e "Specify wordlist file (try -h)"; fi;
fi

file=$1
check_file=$(exist $file)
check_list=$(exist $wordlist_file)

#execute commands
if [[ $check_file -eq 0 && $check_list -eq 0 ]]
then
	file_type=$(file $file | cut -f2 -d " " )
	echo "File type: $file_type"
	#if file type is zip
	if [[ $file_type == "Zip" ]]
	then
		flag_zip=1
		line=1
		while read word
		do
			unzip -qq -d X -o -P $word $file
			if [ $? -eq 0 ]; then
				echo -e "Found: \e[4m$word\e[0m at line $line"
				flag_zip=0
				break
			fi
			((line++))
		done < $wordlist_file

		if [ $flag_zip -eq 1 ]; then echo "Password not found!!"; fi

	#if file type is 7-zip
	elif [[ $file_type == "7-zip" ]]
	then
		flag_7z=1
		line=1
		while read word
		do
			7z -oX e -p${word} $file -aoa > /dev/null 2>&1
			if [ $? -eq 0 ];then
				echo -e "Found: \e[4m$word\e[0m at line $line"
				flag_7z=0
				break
			fi
			((line++))
		done < $wordlist_file
		if [ $flag_7z -eq 1 ]; then echo "Password not found!!"; fi
	fi
	rm -rf X/
elif [ $check_list -eq 1 ]
then
	echo "Wordlist file: $wordlist_file not found."
else
	echo "Accept file formats zip and 7z."
fi
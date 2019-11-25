#!/bin/bash

echo -n Password to be checked:
read -s input

hash="$(echo -n $input | sha1sum | cut -d ' ' -f 1)"
hash1=${hash:0:5}
hash2=${hash:6}

echo

result="$(wget -U "terrible test code" -q -O - https://api.pwnedpasswords.com/range/${hash1} | grep -i $hash2 | cut -d ":" -f 2 | sed -e 's/
//g')"

if [ -z "$result" ];
then
   echo "Your password was not found in the list of compromised passwords"
else
   echo "Your password was found $result times in the list of compromised passwords - you should not use this password. For more information please visit https://haveibeenpwned.com/Passwords"
fi   

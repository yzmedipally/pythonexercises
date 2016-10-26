#!/bin/bash


success=1
while [ "$success" != "0" ]
do
	gitlab-ctl status | grep '^run'	
	success=$?
	if [ "$success" == "0" ]
	then
		echo "gitlab's up and fine!"
	else	
		echo "gitlab's not up yet: $success"
		sleep 5
	fi
done

gitlab-rails console production <<GITLAB_COMMAND_LINE
user = User.where(id: 1).first
user.password = 'test1234'
user.password_confirmation = 'test1234'
user.password_automatically_set = false
user.save!
exit
GITLAB_COMMAND_LINE

curl -I localhost/users/sign_in


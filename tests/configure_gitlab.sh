#!/bin/bash

gitlab-rails console production <<GITLAB_COMMAND_LINE
user = User.where(id: 1).first
user.password = 'test1234'
user.password_confirmation = 'test1234'
user.password_automatically_set = false
user.save!
exit
GITLAB_COMMAND_LINE

curl -I localhost/users/sign_in


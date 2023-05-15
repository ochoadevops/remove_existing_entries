# remove_existing_entries

## Creating The Keys:
``` 
 ssh-keygen -t rsa -f ~/.ssh/emails
 eval "$(ssh-agent -s)"
 ssh-add ~/.ssh/emails
 cat ~/.ssh/emails.pub
``` 

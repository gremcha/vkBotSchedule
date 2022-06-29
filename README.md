Install dependencies:

```
pip install -r requirements.txt
```

Required files:

- creds.json

  - enable sheets API
  - create a service account
  - download your credentials
  - move that file to the root of bot, and rename it to creds.json

- spread.txt

  - this is part of the link with the table
  - the owner of the table must give the account permission to read/edit the desired table

- vkInfo.json

  the token must have permission for messages and the wall of the group

  ```
  {
    "userLogin": *your login(str)*,
    "userPassword": *your password(str)*,
    "groupID": *id your group(int)*,
    "token": *token your group(str)*,
  }
  ```

# Skill sommerzeit for Magenta Speaker

## How it works

[![Sommerzeit Demo](https://img.youtube.com/vi/rx3plVD2waE/0.jpg)](https://youtu.be/rx3plVD2waE)

## Configuration

There are 2 configuration files: `creds.conf` and `skill.conf`.

### Credentials

In `creds.conf` you must add your credentials for your work tools. You need a Microsoft Office 365 administrator account and a Jira account. A special file called `creds.conf` needs to be in the root of the project along with the other configuration file called `skill.conf`.

Please open an issue in the tracking system in order to schedule a demo. However, the following entries are necessary if you want to test it by yourself:
```
[jira]
username = <email of your Jira user>
url = <Atlassian Jira Cloud or Server instance>
secret_token= <secret API token you can get from Jira>

[office365]
username = <Microsoft Office 365 account>
tenant_id = <AD tenant for Office 365>
client_id = <client ID for this app; you must create it in AD>
client_secret = <client secret from AD>
token_dir = <where to store Office365 temporary access tokens, e.g. in /tmp/hackathon_tokens>
```

### Skill settings

In `skill.conf` you can specify:
````
[jira]
nickname = <your nickname, e.g. Andrei>
fullname = <full name>
role = <project-manager | developer | core | crm; only project-manager is implemented so far> 
project = <Jira project, e.g. Hackathon2020>
sprint = <sprint name, e.g. HAC Sprint 1>
team = <team members' names, separated by comma; e.g. Andrei Lihu, Adele Vance, Diego Siciliani, Joni Sherman, Lee Gu>


[office365]
day = <date for Office 365 emails and calendar, e.g. 07.12.2020>

[ml]
summarization_model = <summarization model, e.g. bert-base-german-cased>
````
    

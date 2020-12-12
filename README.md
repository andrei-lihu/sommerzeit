# Skill sommerzeit for Magenta Speaker

## Installation

## Configuration
You need a Microsoft Office 365 administrator account and a Jira account. A special file called `creds.conf` needs to be in the root of the project along with the other configuration file called `skill.conf`.

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

## How to run it
    
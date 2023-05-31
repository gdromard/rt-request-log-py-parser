## Installation 

Prerequisite : Python 3.10+, pip & virtualenv

in the project folder initialize a virtualenv and activate it 

`virtualenv venv`

Activate it

`source ./venv/bin/activate` for Linux / MacOs

Or 

`venv\Scripts\activate` on Windows

Install the dependencies
`pip3 install -r requirements.txt`

Put some request-*.log files in the `logs_to_process` folder and run 

`python3 requestlog-parser.py`

## Log format

```
Timestamp | Trace ID | Remote Address | Username | Request method | Request URL | Return Status | Request Content Length | Response Content Length | Request Duration | Request User Agent
```

The content length fields unit is bytes

Ref : https://jfrog.com/help/r/jfrog-platform-administration-documentation/logging

## Saas logs example => 11 fields

2023-05-28T07:02:20.787Z|331fddde8f0dd2|718.200.380.426|token:jfrt@01e9sdfsfb1|POST|/api/mirror/statuses/message|200|195|0|16|Artifactory/7.59.8 75908900

## Self-hosted logs example => 11 fields

### (request.logs)
2023-05-30T16:55:34.406Z|53eeda7ed66a17d0|718.200.380.426|jffe@01dy4jeqn087qe0z2pye7j0kck|GET|/api/httpsso|200|-1|0|12|JFrog-Frontend/1.42.2
### (request-out.logs) => 10 fields (no user agent, traceId is empty)
2023-05-31T09:54:17.677Z||demo-npm-remote|fakeuser|POST|https://foo.bar/artifactory/api/replications/channels/establishChannel|302|157|138|69

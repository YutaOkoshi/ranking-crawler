ranking-crawler

# for developer

## ! Prerequisite !

- Register with twitter developer to create an app and get a key and token.
  - https://developer.twitter.com/en/portal/dashboard
- Create a GCP service account with editing permissions and download secure.json
  - https://console.cloud.google.com/iam-admin/serviceaccounts

## initial setup
```
# 1. make .env
$ cp .env,example .env

# 2. edit .env
$ vi .env
AFF_TAG=${Amazon Affiliate Tag}
UA=${Any Value}
BUCKET_NAME=${GCP bucket name}

# 3. install python 3.9
$ pyenv local 3.9.2

# 4. create & active virtual env
$ python -m venv venv
$ source venv/bin/activate

# 5. pip install
(venv)$ pip install -r requirements.txt
```


## gcloud deploy from local

```
$ gcloud -v
Google Cloud SDK 340.0.0

$ gcloud functions deploy ranking-crawler-function \
    --trigger-topic "ranking-crawler-topic" \
    --runtime python39 \
    --region=asia-northeast1 \
    --entry-point main \
    --service-account "ranking-crawler@zippy-haven-313702.iam.gserviceaccount.com" \
    --memory 256MB \
    --set-env-vars ENV=PRD
```


## local run

- ! NEED GCP ServiceAccount Credential File !!

```
# save secure.json
# need editing privileges
(venv)$ cp secure.json.example secure.json
(venv)$ vi secure.json

# execution
(venv)$ python cli.py
```

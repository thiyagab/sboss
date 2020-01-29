# sboss
A sample to freely host a telegram bot as cloud functions and integrated with firebase firestore

This project uses firebase-admin and python-telegram-bot sdk.

1. Create a project with Google cloud
2. Create a service user for your project and download the credentials as json file to this working directory, rename it to serviceaccount.json
3. We use this account to update and read the firestore db
4. Setup gcloud cli and login to your project
5. Deploy to google cloud using the following command,

```
$ gcloud beta functions deploy sboss --set-env-vars "TELEGRAM_TOKEN=000:yyy" --runtime python37 --trigger-http
```


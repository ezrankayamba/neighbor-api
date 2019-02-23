# Neighbor App Server

- SMS Config:
  - Env: <code>export SMS_SENDING_APK_KEY=1b73b77444f5f421d4742a743b6582046453c1352d84b00687ae63b29fe862f8 && export SMS_SENDING_URL=https://api.africastalking.com/version1/messaging && export SMS_SENDING_USERNAME=neighborapp</code>
  - Flask App: <code>export FLASK_APP=run.py</code>
  - 1st time: <code>flask db init && flask db migrate && flask db upgrade</code>
  - Upgrade: <code>flask db migrate && flask db upgrade</code>

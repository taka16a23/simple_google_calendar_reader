#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""simple_google_calendar_reader --

"""
import pathlib
import datetime

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class SimpleGoogleCalendarReader(object):
    """SimpleGoogleCalendarReader

    SimpleGoogleCalendarReader is a object.
    Responsibility:
    """
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", ]

    def __init__(self, token_path, secret_path, calender_id):
        self._token_path = token_path
        self._secret_path = secret_path
        self._calender_id = calender_id

    def _get_credentials(self, ):
        # トークンファイルが存在する場合
        if self._token_path.exists() == True:
            # トークン読み込み
            creds = Credentials.from_authorized_user_file(self._token_path, self.SCOPES)
            # トークン有効期限切れ
            if not creds.valid and creds.expired:
                # トークン更新
                creds.refresh(Request())
            return creds
        # トークンが存在しなければ、シークレット読み込み
        flow = InstalledAppFlow.from_client_secrets_file(self._secret_path, self.SCOPES)
        # ブラウザ認証
        creds = flow.run_local_server(open_browser=False)
        # 返却
        return creds

    def get_credentials(self, ):
        creds = self._get_credentials()
        with open(self._token_path, "w") as token:
            token.write(creds.to_json())
        return creds

    def read(self, time_min, max_results=10, order_by="startTime"):
        creds = self.get_credentials()
        service = build("calendar", "v3", credentials=creds)
        return service.events().list(
            calendarId=self._calender_id,
            timeMin=time_min,
            maxResults=max_results,
            singleEvents=True,
            orderBy=order_by,).execute().get('items', [])



# For Emacs
# Local Variables:
# coding: utf-8
# End:
# simple_google_calendar_reader.py ends here

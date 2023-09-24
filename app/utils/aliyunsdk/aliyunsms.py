# -*- coding: utf-8 -*-
import sys
import uuid
import json
from .aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from .aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT


ACCESS_KEY_ID = "LTAI5tK8dN1zTULs7xtUHRSQ"
ACCESS_KEY_SECRET = "xNCTkckkJcauSpVPgN1pI0dzBHb4vm"

REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"


acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(phone_numbers,code):
    business_id = uuid.uuid1()
    sign_name = '林渭彬的博客'
    template_code = 'SMS_267955538'
    template_param = json.dumps({"code":code})
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    smsRequest.set_OutId(business_id)
    smsRequest.set_SignName(sign_name)
    smsRequest.set_PhoneNumbers(phone_numbers)
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse

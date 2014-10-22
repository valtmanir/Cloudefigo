#!/usr/bin/python
from Common import Logger

__author__ = 'nirv'

import urllib2
import hashlib
import json
from Common.Logger import Logger

class EnvronmentVarialbes:

    @staticmethod
    def get_current_instance_name():
        #return "i-a475724a"
        return urllib2.urlopen("http://169.254.169.254/latest/meta-data/instance-id").read()

    @staticmethod
    def get_current_instance_mac():
        #return "1111"
        return urllib2.urlopen("http://169.254.169.254/latest/meta-data/mac").read()

    @staticmethod
    def get_bucket_unique_id(prefix):
        unique_string_hash = hashlib.sha1(EnvronmentVarialbes.get_current_instance_name()).hexdigest()
        uppercase_result = "{}-{}".format(prefix, unique_string_hash)
        return uppercase_result.lower()

    @staticmethod
    def get_current_instance_profile():
        #return "cloudsec-69378f83fca04e3f9d17af6621f27d3a"
        response = urllib2.urlopen("http://169.254.169.254/latest/meta-data/iam/info").read()
        parsed_response = json.loads(response)
        profile_arn = parsed_response["InstanceProfileArn"]
        iam_arn_list = profile_arn.split("/")
        return iam_arn_list[len(iam_arn_list) - 1]

    @staticmethod
    def get_instance_credentials():
        #return "ASIAJ6FDZWB4RRMBIXLQ aP+61C6DFexLnvzl5bkMUR8A18dDpeLR0d8No9dQ AQoDYXdzEGMa0AMfhzRn2zACISwvZrlIxv2xX8kGWAxsmQdGAVmIslKRoq/mwhqJfmh0zHH5iefr8VdnrMEN0rAPuz00gvSUqAjMcy9wHmYA7r61nBoRToliWhb3v/NajJUSRjiniMqAgS1jGrnBTMCoMTCMGKeBoqPICI22ohOrnc6BO0Qqnu8f9jkmJMQOrBfU3PlVxT4upgVIraQiKf9JVgbWxELmpvzaKicyRxeMreFYrU3ovLyVmZAXd8c2+kmfE7JBVRPgdTRukPRX2iTMkf4W5XcAlcIPKYG2lQdxZM4Oj2X7aPA00WswnU5b2L8+QZFC/EquipZlKx6ZOck9mrfFT2EbewRQYMZGc8nm8JFx+CKSoJsDNDwexFRWChqic28UE7nWJLIX4DfAJQk+t79pblQw79tvA9SD1zB5ziEFf7cJWNgAqCJXwfGHUVvDIRYaZr5TKyFpB7s9axknVyFvWec7Nh7rnzyGSI3Hqqu+L9UuzbKJpnWQ9F+vZhf4NNioJOhCbsf09vom60QIdb2Y45TMEg3TeoAvjHMxuM7OQKvi/VsR5yLwYnhp9bnxg8IbgBlU1QDQXmSgBQ3MG4cwbVRdJf057DcYVAYim2eKCd5QvZMnDiDA4p+iBQ=="
        try:
            role_name = EnvronmentVarialbes.get_current_instance_profile();
            creds_url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/{}".format(role_name)
            response = urllib2.urlopen(creds_url).read()
            parsed_response = json.loads(response)
            boto_cfg_access_key_value = parsed_response["AccessKeyId"]
            boto_cfg_secret_key_value = parsed_response["SecretAccessKey"]
            boto_cfg_token = parsed_response["Token"]
            return "{} {} {}".format(boto_cfg_access_key_value, boto_cfg_secret_key_value, boto_cfg_token)
        except:
            Logger.log("error","Cannot get instance credentials from {}".format(creds_url))
            raise
import re
import boto3


def validate_full_name(full_name):
    """
    Validates the name of the user
    :param full_name:
    :return:
    """
    return bool(full_name.strip())


def validate_mob_num(mob_num):
    """
    Validates the Mobile number
    :param mob_num:
    :return:
    """
    if re.match(r'^(\+91|0)?[6789]\d{9}$', mob_num):
        return mob_num[-10:]
    return False


def validate_pan_num(pan_num):
    """
    Validates the pan Number format
    :param pan_num:
    :return:
    """
    return pan_num.isupper() and re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num)


def validate_manager(manager_id):
    """
    Validates if manager_id is present and active in the manager table
    :param manager_id:
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('manager-table')
    response = table.get_item(Key={'manager_id': manager_id})
    if 'Item' not in response:
        return False
    return response['Item']['is_active']

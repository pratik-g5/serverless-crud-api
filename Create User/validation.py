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
    if manager_id is None:
        return True
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('manager-table')
    response = table.get_item(Key={'manager_id': manager_id})
    if 'Item' not in response:
        return False
    return response['Item']['is_active']


def validate_user_info(user_data):
    if not (validate_full_name(user_data.get('full_name', '')) and
            validate_mob_num(user_data.get('mob_num', '')) and
            validate_pan_num(user_data.get('pan_num', ''))):
        return False
    return True


def update_user_info(user_info, update_data):
    """
    Update user information with the provided update data.

    """
    # Update user info with the provided update_data
    for key, value in update_data.items():
        if key in user_info:
            user_info[key] = value

    return user_info

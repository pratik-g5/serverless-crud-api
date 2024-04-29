import boto3
from user import UserData


def create_user_table(user_data: UserData) -> str:
    """
    Add the newly created user details.
    :param user_data:
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    item = {
        'user_id': user_data.id,
        'full_name': user_data.full_name,
        'mob_num': user_data.mob_num,
        'pan_num': user_data.pan_num,
        'manager_id': user_data.manager_id,
        'created_at': str(user_data.created_at),
        'last_updated': str(user_data.last_updated),
        'is_active': user_data.is_active
    }

    if user_data.manager_id:
        item['manager_id'] = user_data.manager_id

    table.put_item(Item=item)
    return user_data.id


def get_all_users_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    response = table.scan()

    all_users_info = response['Items']
    return all_users_info


def get_user_info_by_user_id(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    response = table.get_item(Key={'user_id': user_id})

    user_info = response.get('Item')
    return user_info

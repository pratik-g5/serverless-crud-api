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
        'is_active': user_data.is_active
    }

    if user_data.manager_id:
        item['manager_id'] = user_data.manager_id

    table.put_item(Item=item)
    return user_data.id

import boto3
from boto3.dynamodb.conditions import Attr

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


def get_users_by_manager_id(manager_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    response = table.scan(
        FilterExpression=Attr('manager_id').eq(manager_id)
    )

    users = response['Items']
    return users


def delete_user_by_user_id(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    try:
        table.delete_item(Key={'user_id': user_id})
        return True
    except Exception as e:
        print(f"Error deleting user with user_id {user_id}: {e}")
        return False


def save_updated_user_info(updated_user_info):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-table-v1')

    try:
        table.update_item(
            Key={'user_id': updated_user_info['user_id']},
            UpdateExpression='SET full_name = :fn, mob_num = :mn, pan_num = :pn, manager_id = :mid, updated_at = :ua',
            ExpressionAttributeValues={
                ':fn': updated_user_info['full_name'],
                ':mn': updated_user_info['mob_num'],
                ':pn': updated_user_info['pan_num'],
                ':mid': updated_user_info['manager_id'],
                ':ua': updated_user_info['updated_at']
            }
        )
    except Exception as e:
        print(f"Error updating user info: {e}")

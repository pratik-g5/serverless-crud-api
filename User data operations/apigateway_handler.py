import json
from datetime import datetime

from validation import validate_manager, update_user_info, validate_user_info
from user_table import create_user_table, get_user_info_by_user_id, get_all_users_info, get_users_by_manager_id, \
    delete_user_by_user_id, save_updated_user_info
from user import UserData


def handle_create_user(event, context):
    """
    handle create user
    """
    body = json.loads(event['body'])

    user_data = UserData(
        id='',
        full_name=body.get('full_name'),
        mob_num=body.get('mob_num'),
        pan_num=body.get('pan_num'),
        manager_id=body.get('manager_id')
    )

    user_data.generate_id()

    manager_id = body.get('manager_id')
    if not validate_manager(manager_id):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid manager_id'})
        }

    if not validate_user_info(user_data):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input data'})
        }

    user_id = create_user_table(user_data)

    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User created successfully', 'user_id': user_id})
    }


def handle_get_user(event, context):
    """
    Get user information
    :param event:
    :param context:
    :return:
    """
    path_params = event.get('pathParameters', {})
    if path_params:
        id = path_params.get('user_id')

        if validate_manager(id):
            users = get_users_by_manager_id(id)
            if not users:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'No users found with the provided manager_id'})
                }

            return {
                'statusCode': 200,
                'body': json.dumps({'users': users})
            }

        user_info = get_user_info_by_user_id(id)

        if not user_info:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User with provided user_id does not exist'})
            }
        return {
            'statusCode': 200,
            'body': json.dumps({'user_info': user_info})
        }

    all_users_info = get_all_users_info()

    return {
        'statusCode': 200,
        'body': json.dumps({'all_users_info': all_users_info})
    }


def handle_delete_user(event, context):
    """
    Delete the user info of provided user_id
    :param event:
    :param context:
    :return:
    """
    body = json.loads(event['body'])
    user_id = body.get('user_id')

    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'user_id is required in the request body'})
        }

    user_info = get_user_info_by_user_id(user_id)

    if not user_info:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User with provided user_id does not exist'})
        }

    if delete_user_by_user_id(user_id):
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'User with user_id {user_id} deleted successfully'})
        }


def handle_update_user(event, context):
    """
    update user info for provided user_id and just the manager for list of user_ids
    :param event:
    :param context:
    :return:
    """
    body = event
    user_ids = body.get('user_ids', [])
    update_data = body.get('update_data', {})
    if 'manager_id' in update_data:
        if not validate_manager(update_data['manager_id']):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid manager_id provided'})
            }
    if len(user_ids) > 1 and any(key for key in update_data if key != 'manager_id'):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Bulk updates can only modify the manager_id key'})
        }

    updated_users = []
    for user_id in user_ids:
        user_info = get_user_info_by_user_id(user_id)
        if not user_info:
            continue
        updated_user_info = update_user_info(user_info, update_data)
        updated_users.append(updated_user_info)

    for user_data in updated_users:
        if not validate_user_info(user_data):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Validation failed for updated data'})
            }

        if 'manager_id' in update_data:
            pass

        user_data['last_updated'] = str(datetime.now())
        save_updated_user_info(user_data)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Users updated successfully'})
    }

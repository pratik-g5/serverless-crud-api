import json
from validation import validate_full_name, validate_mob_num, validate_pan_num, validate_manager
from user_table import create_user_table, get_user_info_by_user_id, get_all_users_info
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

    if not (validate_full_name(user_data.full_name) and
            validate_mob_num(user_data.mob_num) and
            validate_pan_num(user_data.pan_num)):
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

    path_params = event.get('pathParameters', {})
    if path_params:
        user_id = path_params.get('user_id')
        user_info = get_user_info_by_user_id(user_id)
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

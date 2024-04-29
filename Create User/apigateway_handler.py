import json
from validation import validate_full_name, validate_mob_num, validate_pan_num
from user_table import create_user_table
from user import UserData


def lambda_handler(event, context):
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

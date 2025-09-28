def lambda_handler(event, context):
    from app.main import handler

    return handler(event, context)

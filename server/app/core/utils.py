
def serialize_documnet (document:dict)->dict:
    document = document.copy()

    if '_id' in document:
        document['id'] = str(document['_id'])

    return document
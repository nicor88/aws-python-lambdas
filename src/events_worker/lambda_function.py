import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

event = dict()
event['events'] = [
    {'name': 'user:created', 'event_id': 1},
    {'name': 'user:updated', 'event_id': 1},
    {'name': 'account:created', 'event_id': 1},
    {'name': 'campaign:created', 'event_id': 1},
    {'name': 'video:watched', 'event_id': 1},
    {'name': 'user:created', 'event_id': 1},
    {'name': 'request:performed', 'event_id': 1}
]


def add_type(event):
    event['event_type'] = event['name'].split(':')[0]
    return event


def group_dict(type_name):
    group = {'event_type': type_name, 'events': []}
    # TODO for each event_type find the best state machine to start
    return group


def add_events_to_group(*, events, event_types):
    groups = [group_dict(t) for t in event_types]
    for e in events:
        logger.debug(e)
        for g in groups:
            if e['event_type'] == g['event_type']:
                g['events'].append(e)
    return groups


def lambda_handler(event, context):
    events = event['events']
    # TODO validate events
    events_validate = events
    events_with_type = [add_type(e) for e in events_validate]
    event_types = list(set([e['event_type'] for e in events_with_type]))
    events_groups = add_events_to_group(events=events_with_type, event_types=event_types)
    for g in events_groups:
        print(g)
    return 'events processed'


lambda_handler(event, '')

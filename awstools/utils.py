
def filter(name, *values):
    return {'Name': name, 'Values': values}

def tag_filter(name, *values):
    return {'Name': 'tag:'+name, 'Values': values}

def running_filter():
    return filter('instance-state-name', 'running')

def environment_filter(environment):
    return tag_filter('environment', environment)

def region_filter(region):
    return tag_filter('region', region)

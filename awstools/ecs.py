import boto3
from utils import *
import argparse
import functools

class ECS(object):
    def __init__(self, name, region, key):
        self.name = name
        self.ec2 = boto3.resource('ec2', region)
        self.key = key

    def ssh_config(self):
        agents = self.ec2.instances.filter(Filters=running_agents(self.name))
        bastionip = list(self.ec2.instances.filter(Filters=running_bastion(self.name)).limit(1))[0].public_ip_address
        i=0; cmd="";
        for agent in agents:
            cmd += ssh_tpl(i, agent.private_ip_address, bastionip, self.key)
            i+=1
        print(cmd)
        print('# usage ssh -F config ecs<index>')

    @staticmethod
    def config_parser(subparsers):
        # boilerplate
        parser = subparsers.add_parser('ecs')
        parser.set_defaults(func=ECS.execute)
        # args
        parser.add_argument(
            'region',
            help='region of ECS cluster environment',
            default='us-east-1'
        )
        parser.add_argument(
            'cluster',
            help='Name of the ECS cluster environment',
            default='development'
        )
        parser.add_argument(
            'key',
            help='Name of keypair for ECS cluster instances',
            default='development'
        )

    @staticmethod
    def execute(args):
        ECS(
            args.cluster,
            args.region,
            args.key
        ).ssh_config()

# FILTERS
def ecs_agent_filter():
    return tag_filter('ecs_agent', 'true')

def ecs_bastion_filter():
    return tag_filter('ecs_bastion', 'true')

def running_bastion(environment):
    return [
        running_filter(),
        environment_filter(environment),
        ecs_bastion_filter()
    ]

def running_agents(environment):
    return [
        running_filter(),
        environment_filter(environment),
        ecs_agent_filter()
    ]

def ssh_tpl(index, agentip, bastionip, key):
    return """
Host ecs{0}
    Hostname {1}
    User  ec2-user
    ProxyCommand ssh -i {3} -W %h:%p ec2-user@{2}
    IdentityFile {3}""".format(index, agentip, bastionip, key)

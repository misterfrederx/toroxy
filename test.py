import pprint

import configparser
from orchestrator import Orchestrator
from privoxy import PrivoxyWrapper
from tor import TorWrapper

torrc_file = '/home/misterfrederx/Projects/toroxy/tors/tor_1/torrc'
privoxy_file = '/home/misterfrederx/Projects/toroxy/privoxies/privoxy_1/config'

o = Orchestrator('/home/misterfrederx/Projects/toroxy/privoxies/privoxy')

new_member = o.create_new()

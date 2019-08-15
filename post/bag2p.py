#!/usr/bin/env python
import math
import pickle
import yaml
import argparse
import logging
import sys
import os

import rosbag


class Object(object):
    '''
    Blank object for storing data
    '''
    pass


def get_msg_fields(msg):
    ign_list = ['header', 'deserialize','deserialize_numpy','serialize','serialize_numpy']
    good_types = [float,int]
    fields = []
    rfields = []
    for d in dir(msg):
        if ( (not (d in ign_list)) and (not (d[0]=='_')) ):
            if 'msg' in str(type(getattr(msg,d))):
                rfields.append(d)
            elif type(getattr(msg,d)) in good_types:
                fields.append(d)
                
            else:
                print("Warning - ignoring msg field <%s> of type <%s>"%
                      (d,str(type(getattr(msg,d)))))
                
    return (fields, rfields)

def init_datastruct(msg):
    '''
    Return a nested Objects
    '''
    fields, rfields = get_msg_fields(msg)
    data = Object() 
    for f in fields:
        setattr(data,f,[])
    for r in rfields:
        setattr(data,r,init_datastruct(getattr(msg,r)))
    # Add a time field
    setattr(data,'t',[])
    return data
    
def append_msg_data(struct,t,msg):
    fields, rfields = get_msg_fields(msg)
    for f in fields:
        getattr(struct,f).append(getattr(msg,f))
    for r in rfields:
        append_msg_data(getattr(struct,r),None,getattr(msg,r))
    # Time
    if not t is None:
        getattr(struct,'t').append(t)

fname='/home/bsb/Documents/annie_control_aug2019/data/20190814_annie_blue_arrow_testing/operational_logs/stefan_tests/2019-08-14-14-32-21.bag'

def main(argv=None):
    # This enables us to invoke this function with arguments from a script
    if argv is None:
        argv = sys.argv

    # Define our arguments
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class = \
                                         argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename',type=str,help="File name")
    default_loglevel=logging.WARNING
    group = parser.add_argument_group("Verbosity settings")
    group.add_argument('-l', '--logginglevel',
                       help="Set logging level.  Accepts a numeric value {0-50} or a "
                            "string {CRITICAL,ERROR,WARNING,INFO,DEBUG}",
                       dest="loglevel",
                       default=default_loglevel)

    group.add_argument('-d', '--debug',
                       help="Print lots of debugging statements by setting the logging level to DEBUG",
                       action="store_const",
                       dest="loglevel",
                       const=logging.DEBUG,
                       default=logging.WARNING)

    group.add_argument('-v', '--verbose',
                       help="Be verbose by setting the logging level to INFO",
                       action="store_const",
                       dest="loglevel",
                       const=logging.INFO)

    args = parser.parse_args()
    
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y%m%dT%H%M%SZ')
    logging.getLogger().setLevel(args.loglevel)
    logging.info("effective log level:    %s", logging.getLevelName(logging.getLogger().getEffectiveLevel()))

    dirname, fname = os.path.split(args.filename)
    pfname = os.path.join(dirname,fname+'.p')

    logging.info("Reading bag file <%s> and pickling file to <%s>"%(args.filename, pfname))
    
    #info_dict = yaml.load(rosbag.Bag(fname, 'r')._get_yaml_info())

    data = Object()
    bag = rosbag.Bag(args.filename)
    for topic, msg, t in bag.read_messages(topics=['/cmd_vel', '/jacm_gps_dynamics']):
        # If not already initialized
        field = topic.replace('/','')
        if not hasattr(data,field):
            setattr(data, field, init_datastruct(msg))
            
        append_msg_data(getattr(data,field),t.to_sec(),msg)


    bag.close()

    # Save
    pickle.dump(data, open(pfname,"w"))
                 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard interruption - Exiting...")
        


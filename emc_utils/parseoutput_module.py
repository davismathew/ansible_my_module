import clitable
from emc_utils.jsonfilter_util import JSONFilter


class Error(Exception):
  """Base class for errors."""


class IndexTableError(Error):
  """General INdexTable error."""


class CliTableError(Error):
  """General CliTable error."""

def clitable_to_dict(cli_table):
    """Converts TextFSM cli_table object to list of dictionaries
    """
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)

    return objs



def get_structured_data(rawoutput, params ):

#    self.rawoutput=rawoutput
#    self.params=params

    index_file = params['index_file']
    template_dir = params['template_dir']
#    index_file='index'
#    template_dir='/Users/davis.kuriakose/PycharmProjects/ntc-ansible/ntc-templates/templates'
    cli_table = clitable.CliTable(index_file, template_dir)

    attrs = dict(
#        Command='show version',
#        Platform='cisco_ios'
        Command=params['command'],
        Platform=params['platform']
    )
    try:
        cli_table.ParseCmd(rawoutput, attrs)
        structured_data = clitable_to_dict(cli_table)

    except CliTableError as e:
        # Invalid or Missing template
        # module.fail_json(msg='parsing error', error=str(e))
        # rather than fail, fallback to return raw text
        structured_data = [rawoutput]

    return structured_data


def parse_raw_output( rawoutput, argument_spec):
    """Returns a dict if using netmiko and list of dicts if using trigger
    """
#    self.rawoutput=rawoutput
#    self.argument_spec=argument_spec

    structured_data_response_list = []
    structured_data = {}
    structured_data = get_structured_data(rawoutput, argument_spec)

    return structured_data or structured_data_response_list


def parseoutput(rawtxt, argument_spec):
    #parse method is invoked
    testvar = parse_raw_output(rawtxt, argument_spec)

    print rawtxt
#    testvar[''] = "test"


    newvar=testvar
    return testvar


def compareoutput(bef_variable,aft_variable,params_compared,command):
    jfilter = JSONFilter()

    return jfilter.compare_json(bef_variable,aft_variable,params_compared,command)
#    return params_compared


if __name__ == "__main__":


    argument_spec=dict(platform='cisco_ios',
                    index_file='index',
#                    template_dir='ntc-templates/templates',
                    template_dir='/home/davis/Documents/temp/textfsm-parsing/ntc-templates/templates',
                    command='show version',
                    host='',
                    port=dict(default=22, required=False),
                    username='cisco',
                    password='cisco',
                    secret=dict(required=False, type='str')
                       )


    rawtxt="""Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500-ENTSERVICESK9-M), Version 12.2(31)SGA1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2007 by Cisco Systems, Inc.
Compiled Fri 26-Jan-07 14:28 by kellythw
Image text-base: 0x10000000, data-base: 0x118AD800

ROM: 12.2(31r)SGA
Pod Revision 0, Force Revision 34, Gill Revision 20

router.abc uptime is 3 days, 13 hours, 53 minutes
System returned to ROM by reload
System restarted at 05:09:09 PDT Wed Apr 2 2008
System image file is "bootflash:cat4500-entservicesk9-mz.122-31.SGA1.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to export@cisco.com.

cisco WS-C4948-10GE (MPC8540) processor (revision 5) with 262144K bytes of memory.
Processor board ID FOX111700ZP
MPC8540 CPU at 667Mhz, Fixed Module
Last reset from Reload
2 Virtual Ethernet interfaces
48 Gigabit Ethernet interfaces
2 Ten Gigabit Ethernet interfaces
511K bytes of non-volatile configuration memory.

Configuration register is 0x2102

"""
    #print argument_spec['template_dir']
    params=dict()
    print parseoutput(rawtxt,argument_spec)
    # getvars_file()

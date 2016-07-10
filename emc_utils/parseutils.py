import json
from ansible import errors
class Error(Exception):
    """

    """
class ConstructvarError(Exception):
    """

    """

def getvars_file(command,file):
    try:
        with open(file) as data_file:
            data=json.load(data_file)
    except:
        raise errors.AnsibleFilterError('file parse error')
#        return "file parse error"
    varlist=[]
    try:
        for key,value in data[command].iteritems():
            if (data[command][key] == "yes"):
                varlist.append(key)
    except:
        raise errors.AnsibleFilterError('key list error')
    return varlist

def construct_var(variableb, variablea, command):
    base_path='/etc/'
    file='/home/davis/Documents/networkaut/disp.json'
    varb={}
    vara={}
    olddict={}
    newdict={}
    innerlist=[]
    varlist = getvars_file(command,base_path+'disp.json')
    try:
        for ele in varlist:
            varb[ele]=variableb[ele]
            vara[ele]=variablea[ele]
        innerlist = [vara, varb]
    except:
        raise errors.AnsibleFilterError('error in construct_var')
#        return "error in construct_var"
    varb={}
    vara={}

    return innerlist

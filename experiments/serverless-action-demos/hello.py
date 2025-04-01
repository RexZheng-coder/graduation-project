import sys
def main(dict):
    if 'name' in dict:
        name = dict['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "!"
    version = sys.version
    print(greeting)
    print(version)
    return {"greeting": greeting, "version": version}


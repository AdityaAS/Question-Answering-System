import sys
import errno
import ConfigParser
import web
from causeofwhy import indexer

CONFIG_FNAME = 'causeofwhy.ini'

def create_default_config():
    config = ConfigParser.SafeConfigParser()
    config.add_section('wiki')
    config.set('wiki', 'location', 'PATH/TO/WIKIPEDIA/DUMP.xml')
    config.add_section('web server')
    config.set('web server', 'port', '8080')
    with open(CONFIG_FNAME, mode='w') as f:
        config.write(f)

def read_config():
    config = ConfigParser.SafeConfigParser()
    try:
        with open(CONFIG_FNAME) as f:
            config.readfp(f)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        print 'Configuration file not found! Creating one...'
        create_default_config()
        print 'Please edit the config file named: ' + CONFIG_FNAME
        sys.exit(errno.ENOENT)
    return config

def load_index(wiki_location, doci_in_memory=False):
    try:
        return indexer.Index(wiki_location, doci_in_memory)
    except indexer.IndexLoadError:
        indexer.create_index(wiki_location)
        return indexer.Index(wiki_location, doci_in_memory)

def main():
    config = read_config()
    print 'Starting web server'
    web.main(index, int(config.get('web server', 'port')))

if __name__ == '__main__':
    sys.exit(main())
    

import os
import sys
import time
import random
import threading
import client

class PutClass(threading.Thread):
    def __init__(self, name, prefix, ops, storage_url, token, container_name, data):
        threading.Thread.__init__(self)
        self.prefix = prefix
        self.data = data
        self.url = storage_url
        self.token = token
        self.container_name = container_name
        self.ops = ops
        self.name = "PUT-%s" % name
    def run(self):
        for x in range(self.ops):
            obj_name = "%s%s" % (self.prefix, str(random.random()))
            try:
                s_time = time.time()
                client.put_object(self.url, self.token, self.container_name, obj_name, self.data)
                e_time = time.time()
                if (e_time - s_time) > 2.0:
                    log_info("%s took longer than 2s: %.02fsec %s %s %s %s" % (self.name, (e_time - s_time), self.url, self.token, self.container_name, obj_name))
            except client.ClientException as e:
                log_info("error on PUT: %s %s %s" % e.http_status, e.http_reason, e.http_path)
                
class GetClass(threading.Thread):
    def __init__(self, name, ops, storage_url, token, container_name, objs):
        threading.Thread.__init__(self)
        self.objs = objs
        self.url = storage_url
        self.token = token
        self.container_name = container_name
        self.ops = ops
        self.name = "GET-%s" % name
    def run(self):
        for x in range(self.ops):
            obj_name = self.objs[x]
            try:
                s_time = time.time()
                foo = client.get_object(self.url, self.token, self.container_name, obj_name)
                e_time = time.time()
                if (e_time - s_time) > 2.0:
                    log_info("%s took longer than 2s: %.02fsec %s %s %s %s" % (self.name, (e_time - s_time), self.url, self.token, self.container_name, obj_name))
            except client.ClientException as e:
                log_info("error on GET: %s %s %s" % e.http_status, e.http_reason, e.http_path)
                
def log_info(text):
    f = open("errors.txt", 'a')
    f.write("%s\n" % text)
    f.close()

def put_test(procs, ops, storage_url, token, container_name, size, data):
    print "Starting PUTs %s procs %s ops, %sk of data" % (procs, ops, size)
    prefix = "%s%s%s" % (procs, ops, size)
    start_put = time.time()
    put_threads = []
    for i in range(procs):
        t = PutClass(i, prefix, ops, storage_url, token, container_name, data)
        t.start()
        put_threads.append(t)
    [t.join() for t in put_threads]
    end_put = time.time()
    return str(end_put - start_put)
    
def get_test(procs, ops, storage_url, token, container_name, size):
    print "Starting GETs %s procs %s ops, %sk of data" % (procs, ops, size)
    prefix = "%s%s%s" % (procs, ops, size)
    get_threads = []
    objs = [o['name'] for o in client.get_container(storage_url, token, container_name, prefix=prefix)[1]]
    start_get = time.time()
    for i in range(procs):
        t = GetClass(i, ops, storage_url, token, container_name, objs)
        t.start()
        get_threads.append(t)
    [t.join() for t in get_threads]
    end_get = time.time()
    return str(end_get - start_get)

if __name__ == "__main__":
    if not (os.environ.has_key('CF_USER') and os.environ['CF_KEY']):
        sys.exit("please set the CF_USER and CF_KEY environment variables to your cloudfiles credentials")
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-t', '--threads', dest='threads', type='int', default=5, help="number of threads")
    parser.add_option('-o', '--ops', dest='ops', type='int', default=10, help="number of operations per thread")
    parser.add_option('-s', '--size', dest='size', type='int', default=32, help="size of object in kB")
    parser.add_option('--no-get', dest='no_get', action="store_false", default=True, help="skip get")
    (options, args) = parser.parse_args(sys.argv)

    auth_url = "https://auth.api.rackspacecloud.com/v1.0"
    storage_url, token = client.get_auth(auth_url, os.environ['CF_USER'], os.environ['CF_KEY'])
    
    c = "cf_speed_test_%s" % str(random.random())
    try:
        client.get_container(storage_url, token, c)
    except client.ClientException, e:
        if e.http_status == 404:
            client.put_container(storage_url, token, c)
    
    fp = open('/dev/random', 'r')
    data = fp.read(options.size*1024)
    fp.close()
    
    fp = open('errors.txt', 'a')
    fp.write("new test %s\n" % c)
    fp.close()
    
    print "testing with container %s" % c
    
    stats = [options.threads, options.ops, options.size, storage_url, c]
    print stats
    put_time = put_test(options.threads, options.ops, storage_url, token, c, options.size, data)
    print "*** %s threads, %s put operations w/%sk data took %s ***" % (options.threads, options.ops, options.size, put_time)
    if options.no_get:
        get_time = get_test(options.threads, options.ops, storage_url, token, c, options.size)
        print "*** %s threads, %s get operations w/%sk data took %s ***" % (options.threads, options.ops, options.size, get_time)
        
    fp = open('stats.txt', 'a')
    fp.write("%d, %d, %d, %s, %s, %s, %s\n" % (options.threads, options.ops, options.size, storage_url, c, put_time, get_time))
    fp.close()
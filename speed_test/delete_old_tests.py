import os
import threading
import client

class DeleteClass(threading.Thread):
    def __init__(self, n, url, token, c, objs):
        threading.Thread.__init__(self)
        self.objs = objs
        self.c = c
        self.url = url
        self.token = token
        self.name = n
        print "init thread %s, deleting %s objects from %s" % (n, len(objs), c)
        
    def run(self):
        for o in self.objs:
            try:
                client.delete_object(self.url, self.token, self.c, o)
            except client.ClientException as e:
                print "** ERROR ** %s: %s" % (e.http_status, e.http_reason) 

if __name__ == "__main__":
    auth_url = "https://auth.api.rackspacecloud.com/v1.0"
    storage_url, token = client.get_auth(auth_url, os.environ['CF_USER'], os.environ['CF_KEY'])
    
    containers = [(c['name'], c['count']) for c in client.get_account(storage_url, token, prefix="cf_speed_test")[1]]
    
    for c in containers:
        if int(c[1]) > 0:
            objs = [o['name'] for o in client.get_container(storage_url, token, c[0])[1]]
            for x in range(20):
                d = DeleteClass(x+1, storage_url, token, c[0], objs[x::20])
                d.start()
        else:
            print "ok to delete container %s" % c[0]
            client.delete_container(storage_url, token, c[0])

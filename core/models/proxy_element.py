

class ProxyElement(object):
    
    def __init__(self, element):
        self._element = element
    
    def __getattr__(self, funcname):
        print 'proxyelement'
        return getattr(self._element, funcname)

    def click(self):
        print 'proxyelement click'

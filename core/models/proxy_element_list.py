
from brome.core.models.proxy_element import ProxyElement

class ProxyElementList(list):
    def __init__(self, elements):
        self._elements = elements

    def __getslice__(self, i, j):
        return ProxyElementList(self._elements[i:j])

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        for element in self._elements:
            yield ProxyElement(element)

    def __getitem__(self, index):
        print 'ProxyElementList __getitem__'
        return self._elements[index]

#! -*- coding: utf-8 -*-

from brome.core.model.proxy_element import ProxyElement

class ProxyElementList(list):
    def __init__(self, elements, selector, pdriver):
        self._elements = elements
        self._selector = selector
        self.pdriver = pdriver

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __reversed__(self):
        return self.__getitem__(slice(None, None, -1))

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        for element in self._elements:
            yield ProxyElement(element, self._selector, self.pdriver)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return ProxyElementList(self._elements[index.start: index.stop: index.step], self._selector, self.pdriver)
        else:
            return ProxyElement(self._elements[index], self._selector, self.pdriver)

    def __repr__(self):
        if len(self) <= 5:
            return 'WebElement list [\n %s \n]'%',\n '.join([repr(el) for el in self])
        else:
            return 'WebElement list containing %d webelement'%len(self)

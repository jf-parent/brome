#! -*- coding: utf-8 -*-

from brome.core.model.proxy_element import ProxyElement

class ProxyElementList(list):
    def __init__(self, elements, selector):
        self._elements = elements
        self._selector = selector

    def __getslice__(self, i, j):
        return ProxyElementList(self._elements[i:j], self._selector)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        for element in self._elements:
            yield ProxyElement(element, self._selector)

    def __getitem__(self, index):
        print 'ProxyElementList __getitem__'
        return ProxyElement(self._elements[index], self._selector)

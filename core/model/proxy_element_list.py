#! -*- coding: utf-8 -*-

from brome.core.model.proxy_element import ProxyElement

class ProxyElementList(list):
    def __init__(self, elements, selector, pdriver):
        self._elements = elements
        self._selector = selector
        self.pdriver = pdriver

    def __getslice__(self, i, j):
        return ProxyElementList(self._elements[i:j], self._selector, self.pdriver)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        for element in self._elements:
            yield ProxyElement(element, self._selector, self.pdriver)

    def __getitem__(self, index):
        return ProxyElement(self._elements[index], self._selector, self.pdriver)

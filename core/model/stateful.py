class Stateful(object):
    def __getstate__(self):
        dict_ = {}

        for key, value in self.__dict__.iteritems():
            if type(value) in [str, unicode, int, float, dict, list] :
                dict_[key] = value

        return dict_

    @classmethod
    def is_stateful(cls, value):
        if Stateful in value.__class__.__bases__ or \
            type(value) in [int, unicode, str, dict, list, float]:
            return True
        else:
            return False

    @classmethod
    def cleanup_list(cls, list_):
        effective_list = []
        for item in list_:
            if type(item) == list:
                effective_list.append(cls.cleanup_list(item))
            elif type(item) == dict:
                effective_list.append(cls.cleanup_dict(item))
            else:
                ret = cls.is_stateful(item)
                if ret:
                    effective_list.append(item)

        return effective_list

    @classmethod
    def cleanup_dict(cls, dict_):
        effective_dict = {}
        for key, value in dict_.iteritems():
            if type(value) == list:
                effective_dict[key] = cls.cleanup_list(value)
            elif type(value) == dict:
                effective_dict[key] = cls.cleanup_dict(value)
            else:
                ret = cls.is_stateful(value)
                if ret:
                    effective_dict[key] = value

        return effective_dict
        
    @classmethod
    def cleanup_state(cls, state):
        effective_state = {}
        for key, value in state.iteritems():
            if type(value) == list:
                effective_state[key] = cls.cleanup_list(value)
            elif type(value) == dict:
                effective_state[key] = cls.cleanup_dict(value)
            else:
                ret = cls.is_stateful(value)
                if ret:
                    effective_state[key] = value

        return effective_state

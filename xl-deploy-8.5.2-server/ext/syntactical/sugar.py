import java.util as util
from java.lang import Enum 
from com.xebialabs.deployit.plugin.api.udm import ConfigurationItem
from com.xebialabs.deployit.plugin.api.deployment.specification import Delta
from com.xebialabs.deployit.plugin.api.deployment.specification import Deltas
from com.xebialabs.deployit.plugin.api.deployment.specification import DeltaSpecification
from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.deployit.plugin.api.deployment.planning import DeploymentPlanningContext
from com.xebialabs.xlplatform.documentation import PublicApi
from com.xebialabs.xlplatform.documentation import PublicApiRef
from com.xebialabs.xlplatform.utils import ReflectionUtils
import inspect
from sets import Set

class _ProxyWrapper():
    def __init__(self):
        pass

    def wrap(self, item):
        if item is None:
            return None
        if inspect.ismethod(item):
            def wrapped_method(*args):
                return _wrapper.wrap(item(*_unwrapper.unwrap_args(*args)))
            return wrapped_method
        if isinstance(item, Deltas):
            return _BaseProxy(item)
        if isinstance(item, Delta):
            return _DeltaProxy(item)
        if isinstance(item, DeltaSpecification):
            return _DeltaSpecificationProxy(item)
        if isinstance(item, Enum):
            return _AsStringComparatorProxy(item)
        if isinstance(item, Type):
            return _AsStringComparatorProxy(item)
        if isinstance(item, list):
            return self.wrap_collection(item)
        if isinstance(item, util.List):
            return self.wrap_collection(item)
        if isinstance(item, Set):
            return self.wrap_set(item)
        if isinstance(item, util.Set):
            return self.wrap_set(item)
        if isinstance(item, util.Map):
            return self.wrap_map(item)
        if isinstance(item, dict):
            return self.wrap_dictionary(item)
        if isinstance(item, ConfigurationItem):
            return _ConfigurationItemProxy(item)
        if isinstance(item, DeploymentPlanningContext):
            return _BaseProxy(item)
        if ReflectionUtils.isAnnotatedWith(item, PublicApiRef):
            return _BaseProxy(item)
        if ReflectionUtils.isAnnotatedWith(item, PublicApi):
            return _BaseProxy(item)
        return item

    def wrap_collection(self, list):
        wrapped_list = []
        for item in list:
            wrapped_list.append(self.wrap(item))
        return wrapped_list

    def wrap_set(self, myset):
        return Set(self.wrap_collection(myset))

    def wrap_map(self, map):
        wrapped_dict = {}
        for key in map.keySet():
            wrapped_dict[key] = self.wrap(map.get(key))
        return wrapped_dict

    def wrap_dictionary(self, dictionary):
        wrapped_dict = {}
        for key in dictionary.keys():
            wrapped_dict[key] = self.wrap(dictionary[key])
        return wrapped_dict

class _ProxyUnWrapper():
    def __init__(self):
        pass

    def unwrap(self, proxy):
        if proxy is None:
            return None
        if isinstance(proxy, _BaseProxy):
            return proxy._delegate
        elif isinstance(proxy, list):
            return self.unwrap_list(proxy)
        elif isinstance(proxy, util.List):
            return self.unwrap_list(proxy)
        elif isinstance(proxy, Set):
            return self.unwrap_set(proxy)
        elif isinstance(proxy, util.Set):
            return self.unwrap_set(proxy)
        if isinstance(proxy, dict):
            return self.unwrap_dictionary(proxy)
        if isinstance(proxy, util.Map):
            return self.unwrap_map(proxy)
        return proxy

    def unwrap_list(self, wrapped_list):
        list = util.ArrayList()
        for item in wrapped_list:
            list.add(self.unwrap(item))
        return list

    def unwrap_set(self, wrapped_set):
        set = util.HashSet()
        for item in wrapped_set:
            set.add(self.unwrap(item))
        return set

    def unwrap_dictionary(self, wrapped_dictionary):
        map = util.HashMap()
        for key in wrapped_dictionary.keys():
            map.put(key, self.unwrap(wrapped_dictionary[key]))
        return map

    def unwrap_map(self, wrapped_map):
        map = util.HashMap()
        for key in wrapped_map.keySet():
            map.put(key, self.unwrap(wrapped_map.get(key)))
        return map

    def unwrap_args(self, *args):
        resultArgs = []
        for i, arg in enumerate(args):
            resultArgs.append(_unwrapper.unwrap(arg))
        return resultArgs

class _BaseProxy():
    def __init__(self, delegate):
        self.__dict__["_delegate"] = delegate

    def __getattr__(self, name):
        delegate = self.__dict__["_delegate"]
        if name == "_delegate":
            return delegate
        else:
            return _wrapper.wrap(getattr(delegate, name))

    def __setattr__(self, name, value):
        return setattr(self.__dict__["_delegate"], name, _unwrapper.unwrap(value))

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, _BaseProxy):
            return self._delegate == other._delegate
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class _DeltaProxy(_BaseProxy):

    def __getattr__(self, name):
        if name == "deployedOrPrevious":
            if self._delegate.deployed is not None:
                return self.deployed
            else:
                return self.previous
        else:
            return _BaseProxy.__getattr__(self, name)

class _DeltaSpecificationProxy(_BaseProxy):

    def __getattr__(self, name):
        if name == "deployedOrPreviousApplication":
            if self._delegate.deployedApplication is not None:
                return self.deployedApplication
            else:
                return self.previousDeployedApplication
        else:
            return _BaseProxy.__getattr__(self, name)

class _ConfigurationItemProxy(_BaseProxy):

    def __getitem__(self, name):
        return _wrapper.wrap(self._delegate.getProperty(name))

    def __getattr__(self, name):
        delegate = self._delegate
        if name == "values":
            return _ConfigurationItemAsMapProxy(delegate)
        elif delegate.hasProperty(name):
            return _wrapper.wrap(delegate.getProperty(name))
        else:
            return _BaseProxy.__getattr__(self, name)

    def __setattr__(self, name, val):
        if name == "id":
            self._delegate.id = val
        elif name == "values":
            for k in val.keys():
                self._delegate.setProperty(k, val[k])
        else:
            self._delegate.setProperty(name, _unwrapper.unwrap(val))

    def __str__(self):
        return str(self._delegate)

    def __contains__(self, pd_name):
        return self._delegate.hasProperty(pd_name)

class _ConfigurationItemAsMapProxy(_BaseProxy):

    def __setitem__(self, name, val):
        self._delegate.setProperty(name, _unwrapper.unwrap(val))

    def __getitem__(self, name):
        return _wrapper.wrap(self._delegate.getProperty(name))

class _AsStringComparatorProxy(_BaseProxy):

    def __str__(self):
        return str(self._delegate)

    def __eq__(self, other):
        if isinstance(other, _AsStringComparatorProxy):
            return self._delegate == other._delegate
        elif isinstance(other, unicode):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance(other, Enum):
            return self._delegate == other
        else:
            return False

_wrapper = _ProxyWrapper()
_unwrapper = _ProxyUnWrapper()

def wrap(item):
    return _wrapper.wrap(item)

def unwrap(item):
    return _unwrapper.unwrap(item)

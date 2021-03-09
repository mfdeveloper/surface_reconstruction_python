from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
import os
import json


class SurfaceStrategy(ABC):
    """
    Surface Reconstruction base class. Should be implemented by Python/C++
    libraries classes that performs a Poisson surface reconstruction algorithm.

    References:

      - Python strategy pattern: PythonStrategy_.
      - Python interfaces or abstract classes: PythonInterface_.

      .. _PythonStrategy: https://refactoring.guru/design-patterns/strategy/python/example
      .. _PythonInterface: https://realpython.com/python-interface
    """

    parameters = {}

    _parameters_key_values = {}

    def __init__(self, point_cloud_file="", output_file="", filter_script_file="", clean_up=True):
        self.output_file = output_file
        self.filter_script_file = filter_script_file
        self.normals_estimated = False
        self.applied_filters = False

        cls = self.__class__
        cls._parameters_convertion()

        if clean_up and len(output_file) > 0 and os.path.exists(output_file):
            os.remove(output_file)

        if len(point_cloud_file) > 0:
            if not os.path.exists(point_cloud_file):
                raise FileNotFoundError(f'The point cloud file "{point_cloud_file}" was not found')

            self.load_file(point_cloud_file)

    @abstractmethod
    def load_file(self, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def poisson_mesh(self, save_file=True, **params: {}):
        """
        A surface reconstruction triangle method invoked by each library

        :param save_file:
        :param params:
        :return:
        """
        raise NotImplementedError

    def default_parameters(self, return_json=True) -> Union[dict, str]:
        """
        Get all parameters required for all filters/methods to do a
        surface reconstruction.

        :returns Union[dict, str]: A dictionary of parameters by filter/method name
        """
        if return_json:
            return json.dumps(self.parameters)
        else:
            return self.parameters

    def poisson_filters(self, callback: callable, **params: {}):

        # cls = self.__class__

        for name in self._parameters_key_values:

            if 'filters' in params:
                filters = params['filters']

                if not filters[name]:
                    self._parameters_key_values[name] = {}

                if type(filters[name]) is dict:

                    if self._parameters_key_values and type(self._parameters_key_values) is dict:
                        self._parameters_key_values[name].update(filters[name])

            if self._parameters_key_values[name]:
                callback(name, self._parameters_key_values[name])

    @classmethod
    def _parameters_convertion(cls) -> dict:

        for param_name in cls.parameters:
            if type(cls.parameters[param_name]) is list:
                cls._parameters_key_values[param_name] = {item['name']: item['value'] for item in cls.parameters[param_name]}
            elif type(cls.parameters[param_name]) is dict:
                if 'name' in cls.parameters[param_name] and 'value' in cls.parameters[param_name]:
                    cls._parameters_key_values[param_name] = {cls.parameters[param_name]['name']: cls.parameters[param_name]['value']}
                else:
                    cls._parameters_key_values[param_name] = cls.parameters[param_name].copy()

        return cls._parameters_key_values

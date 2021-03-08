from typing import Type, TypeVar
from .singleton_meta import SingletonMeta
from .surface_strategy import SurfaceStrategy
from .pymeshlab_surface import PyMeshlabSurface
from .open3d_surface import Open3dSurface

TStrategy = TypeVar('TStrategy', bound=SurfaceStrategy)


class SurfaceReconstruction(metaclass=SingletonMeta):
    _types = {
      'pymeshlab': PyMeshlabSurface,
      'open3d': Open3dSurface,
      'default': Open3dSurface
    }

    def __new__(cls, *args, **kwargs) -> Type[TStrategy]:
        method = kwargs.get('method_type')
        if not method and 'default' in cls._types:
            method = 'default'

        if method in cls._types:
            return cls._types[method]
        else:
            msg = f"""The method type "{method}" was not registered
              Use {cls.__name__}.{cls.register_type.__name__}() to register this type"""

            raise TypeError(msg)

    @classmethod
    def register_type(cls, type_cls: Type[TStrategy]):
        name = type_cls.__name__.replace('Surface', '').lower()
        if name not in cls._types:
            cls._types[name] = type_cls
        else:
            raise Warning(f'The type "{type_cls.__name__}" was registered!')


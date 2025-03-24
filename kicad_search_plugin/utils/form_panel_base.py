import abc
from enum import Enum

from kicad_search_plugin.order.supported_region import SupportedRegion
from .number_round import number_round


class FormKind(Enum):
    QUERY_PRICE = 0
    PLACE_ORDER = 1


class FormPanelBase:
    def init(self) -> "None":
        pass

    def is_valid(self) -> bool:
        return True

    @abc.abstractclassmethod
    def get_from(self, kind: FormKind) -> "dict":
        pass

    def on_region_changed(self):
        pass


    @staticmethod
    @number_round()
    def convert_geometry(form_kind: FormKind, region: SupportedRegion, geometry: float):
        """Convert the geometry (mm) to proper unit

        Args:
            form_kind (FormKind):
            region (SupportedRegion):
            geometry (float): mm
        """
        if (
            SupportedRegion.CHINA_MAINLAND != region
            and FormKind.PLACE_ORDER == form_kind
        ):
            return geometry
        return geometry / 10

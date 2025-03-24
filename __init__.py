import sys
import os

try:
    PLUGIN_ROOT = os.path.dirname(os.path.abspath(__file__))
    if PLUGIN_ROOT not in sys.path:
        sys.path.append(PLUGIN_ROOT)
    from .kicad_search_plugin.plugin.kicad_amf_action_plugin import KiCadAmfActionPlugin

    KiCadAmfActionPlugin().register()
except Exception as e:
    import logging

    logger = logging.getLogger()
    logger.debug(repr(e))

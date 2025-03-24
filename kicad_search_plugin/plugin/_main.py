DEFAULT_CERTIFICATION = None
if DEFAULT_CERTIFICATION is None:
    import certifi
    import ssl
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
DEFAULT_CERTIFICATION = True
from kicad_search_plugin.settings.single_plugin import SINGLE_PLUGIN


def _main():
    if not SINGLE_PLUGIN.show_existing():
        from kicad_search_plugin.gui.app_base import BaseApp
        
        app = BaseApp()
        if app.load_success():
            app.startup_dialog()


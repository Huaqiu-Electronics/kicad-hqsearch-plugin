from enum import Enum
from .supported_region import SupportedRegion


class URL_KIND(Enum):
    QUERY_PRICE = 0
    PLACE_ORDER = 1
    SMT_QUERY_PRICE = 2
    SMT_PLACE_ORDER = 3


class OrderRegion:
    AVAILABLE_URLS = {
        SupportedRegion.CHINA_MAINLAND: {
            URL_KIND.PLACE_ORDER: "https://www.eda.cn/openapi/api/hqpcb/External/fileQuote",
            URL_KIND.QUERY_PRICE: "https://www.eda.cn/openapi/api/hqpcb/public/ajax_valuation",
            URL_KIND.SMT_QUERY_PRICE: "https://www.eda.cn/openapi/api/smt-hqchip/smtservice/app/price/pricing",
            URL_KIND.SMT_PLACE_ORDER: "https://www.eda.cn/openapi/api/smt-hqchip/userCenterApi/DfmOrder/saveDfmSmtTmpOrder",
        },
        SupportedRegion.EUROPE_USA: {
            URL_KIND.PLACE_ORDER: "https://www.nextpcb.com/Upfile/kiCadUpFile",
            URL_KIND.QUERY_PRICE: "https://www.nextpcb.com/ajax/valuation",
            URL_KIND.SMT_QUERY_PRICE: "https://api.nextpcb.com/assembly/compute/?appid=7d1b25dce0b410dc588181713afe3465",
            URL_KIND.SMT_PLACE_ORDER: "https://api.nextpcb.com/analyze/upfile/?appid=7f94517ab22cdec82cfcbd09bbed1400"
        },
        SupportedRegion.JAPAN: {
            URL_KIND.PLACE_ORDER: "https://jp.nextpcb.com/Upfile/kiCadUpFile",
            URL_KIND.QUERY_PRICE: "https://jp.nextpcb.com/ajax/valuation",
            URL_KIND.SMT_QUERY_PRICE: "https://api.nextpcb.com/assembly/compute/?appid=7d1b25dce0b410dc588181713afe3465",
            URL_KIND.SMT_PLACE_ORDER: "https://api.nextpcb.com/analyze/upfile/?appid=7f94517ab22cdec82cfcbd09bbed1400"
        },
    }

    @staticmethod
    def get_url(region: SupportedRegion, kind: URL_KIND):
        if region in OrderRegion.AVAILABLE_URLS:
            return OrderRegion.AVAILABLE_URLS[region][kind]

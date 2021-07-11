import xmltodict
import json
import logging

logger = logging.getLogger(__name__)


def xml_to_dict_transform(xml: str) -> dict:
    transform = xmltodict.parse(xml)
    logger.info('Original: %s', xml)

    transform_txt = json.dumps(transform)
    logger.info('Transform: %s', transform_txt)
    return transform

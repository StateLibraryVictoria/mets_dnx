from nose.tools import *
from lxml import etree as ET

from mets_dnx import factory as mdf

import os


def test_mets_dnx():
    """Test basic construction of METS DNX"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'pm'),
        modified_master_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'data', 'test_batch_1', 'mm'),
        input_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'test_batch_1'),
        generalIECharacteristics=[{'submissionReason': 'bornDigitalContent', 'IEEntityType': 'periodicIE'}],
        )

    print(ET.tounicode(mets, pretty_print=True))
    

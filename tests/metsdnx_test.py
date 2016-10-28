import json
import os

from nose.tools import *
from lxml import etree as ET

from mets_dnx import factory as mdf


CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

mets_dnx_nsmap = {
    'mets': 'http://www.loc.gov/METS/',
    'dnx': 'http://www.exlibrisgroup.com/dps/dnx'
}

def test_mets_dnx():
    """Test basic construction of METS DNX"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        modified_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'mm'),
        input_dir=os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'data',
            'test_batch_1'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    print(ET.tounicode(mets, pretty_print=True))

    
def test_mets_dnx_with_digital_original_details():
    """Test big fix where true/false value was being populated with uppercase
    inital letter, when translating True or False booleans to strings.
    """
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        modified_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'mm'),
        input_dir=os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'data',
            'test_batch_1'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        digital_original=True
        )
    digital_original_el = mets.xpath('.//key[@id="DigitalOriginal"]')[0]
    assert(digital_original_el.text == "true")


def test_mets_dnx_single_file():
    """Test basic construction of METS DNX for single file"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_single_file_mets(
        ie_dmd_dict=ie_dc_dict,
        filepath=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm',
            'presmaster.jpg'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    print(ET.tounicode(mets, pretty_print=True))


def test_all_amdsec_subsections_have_dnx_element():
    """Make sure that all amdsec have at least a DNX stub element"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_single_file_mets(
        ie_dmd_dict=ie_dc_dict,
        filepath=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm',
            'presmaster.jpg'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    # print(ET.tounicode(mets, pretty_print=True))
    amd_sections = mets.findall("{http://www.loc.gov/METS/}amdSec")
    for section in amd_sections:
        for tag in ('techMD', 'rightsMD', 'sourceMD', 'digiprovMD'):
            subsection = section.find("{http://www.loc.gov/METS/}%s" % tag)
            dnx = subsection.find(".//dnx")
            assert(dnx != None)

def test_structmap_has_version_in_rep_id_for_single_file_sip():
    """test to confirm that a rep's physical structmap has the "-1" at
    the end of it"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_single_file_mets(
        ie_dmd_dict=ie_dc_dict,
        filepath=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm',
            'presmaster.jpg'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    # print(ET.tounicode(mets, pretty_print=True))
    structmap = mets.findall("{http://www.loc.gov/METS/}structMap")[0]
    # print(structmap.tag)
    assert(structmap.attrib["ID"][-2:] == "-1")

def test_structmap_has_version_in_rep_id_for_multi_file_sip():
    """test to confirm that a rep's physical structmap has the "-1" at
    the end of it"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        modified_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'mm'),
        input_dir=os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'data',
            'test_batch_1'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        digital_original=True
        )
    structmap = mets.findall("{http://www.loc.gov/METS/}structMap")[0]
    # print(structmap.tag)
    assert(structmap.attrib["ID"][-2:] == "-1")


def test_mets_dnx_with_cms():
    """Test basic construction of METS DNX, with CMS details"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        cms=[{'recordId': '55515', 'system': 'emu'}],
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        modified_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'mm'),
        input_dir=os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'data',
            'test_batch_1'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    print(ET.tounicode(mets, pretty_print=True))
    cms_id = mets.findall('.//dnx/section[@id="CMS"]/record/key[@id="recordId"]')
    # print(cms_id[0].tag)
    # cms_id = mets.find('.//{http://www.exlibrisgroup.com/dps/dnx}section[@ID="CMS"]/{http://www.exlibrisgroup.com/dps/dnx}record/{http://www.exlibrisgroup.com/dps/dnx}key[@recordId]')
    assert(cms_id[0].text == '55515')


def test_filesec_has_use_attrib_for_single_file_sip():
    """test to confirm that a filesec has the USE="VIEW"
    attribute"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_single_file_mets(
        ie_dmd_dict=ie_dc_dict,
        cms=[{'recordId': '55515', 'system': 'emu'}],
        filepath=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm',
            'presmaster.jpg'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    filegrp = mets.findall(".//{http://www.loc.gov/METS/}fileGrp")[0]
    assert(filegrp.attrib["USE"] == "VIEW")

def test_structmap_for_single_file_mets_has_upper_case_type():
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_single_file_mets(
        ie_dmd_dict=ie_dc_dict,
        cms=[{'recordId': '55515', 'system': 'emu'}],
        filepath=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm',
            'presmaster.jpg'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        )
    structmap = mets.findall(".//{http://www.loc.gov/METS/}structMap")[0]
    # filegrp = mets.findall(".//{http://www.loc.gov/METS/}fileGrp")[0]
    # assert(filegrp.attrib["USE"] == "VIEW")
    assert(structmap.attrib["TYPE"] == "PHYSICAL")
    print(structmap.attrib["TYPE"])
    assert(structmap.attrib["TYPE"] != "Physical")


def test_mets_dnx_with_for_single_rep():
    """
    """
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        input_dir=os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        generalIECharacteristics=[{
            'submissionReason': 'bornDigitalContent',
            'IEEntityType': 'periodicIE'}],
        digital_original=True
        )
    digital_original_el = mets.xpath('.//key[@id="DigitalOriginal"]')[0]
    assert(digital_original_el.text == "true")


def test_mets_dnx_with_json_for_admid_in_filesec_files():
    """For testing new function for building SIP with JSON documents
    describing the structure and metadata of files.
    Specifically testing that all files in the filesec have an ADMID 
    attrib."""
    ie_dc_dict = {"dc:title": "test title"}
    
    pm_json = """[
        {"name": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1"},
         {"name": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_2'),
        digital_original=True)
    print(ET.tounicode(mets, pretty_print=True))
    files_list = mets.findall(".//{http://www.loc.gov/METS/}fileSec"
        "/{http://www.loc.gov/METS/}fileGrp/{http://www.loc.gov/METS/}file")
    for file in files_list:
        assert("ADMID" in file.attrib)
        assert(file.attrib['ADMID'].endswith('-amd'))
    amdsec_list = mets.findall(".//{http://www.loc.gov/METS/}amdSec")
    for amdsec in amdsec_list:
        assert("ID" in amdsec.attrib)
        assert(amdsec.attrib["ID"].endswith("-amd"))
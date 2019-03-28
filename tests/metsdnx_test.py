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
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1"},
         {"fileOriginalName": "img2.jpg",
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


def test_mets_dnx_deriv_copy_gets_preservationType():
    """Test basic construction of METS DNX, but assigning an access derivative
    (using the mm dir for efficiency's sake)"""
    ie_dc_dict = {"dc:title": "test title"}
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'test_batch_1',
            'pm'),
        access_derivative_dir=os.path.join(
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
    ad_pres_type = mets.findall('./{http://www.loc.gov/METS/}amdSec[@ID="rep2-amd"]'
        '/{http://www.loc.gov/METS/}techMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData'
        '/dnx/section[@id="generalRepCharacteristics"]/record/key[@id="preservationType"]'
        )[0]
    assert (ad_pres_type.text == "DERIVATIVE_COPY")
    # print(ad_pres_type)


def test_file_original_path_exists():
    """Test to make sure the fileOriginalPath is added to the
    generalFileCharacteristics sections"""
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
    file_gen_chars_list = mets.findall('.//section[@id="generalFileCharacteristics"]')
    for el in file_gen_chars_list:
        fop = el.findall('./record/key[@id="fileOriginalName"]')
        assert(fop[0].text in ('presmaster.jpg', 'modifiedmaster.jpg'))


def test_gfc_file_label_exists():
    """Test to make sure the label is added to the
    generalFileCharacteristics sections, and that it onlye includes the
    filename up to the extension."""
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
    file_gen_chars_list = mets.findall('.//section[@id="generalFileCharacteristics"]')
    for el in file_gen_chars_list:
        fop = el.findall('./record/key[@id="label"]')
        assert(fop[0].text in ('presmaster', 'modifiedmaster'))
    print(ET.tounicode(mets, pretty_print=True))


def test_structmap_file_label_exists():
    """Test to make sure the label is added to the
    structMap file-level divs, and that it only includes the
    filename up to the extension."""
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
    struct_maps = mets.findall('./{http://www.loc.gov/METS/}structMap')
    for struct_map in struct_maps:
        file_divs = struct_map.findall('.//{http://www.loc.gov/METS/}div[@TYPE="FILE"]')
        for file_div in file_divs:
            assert(file_div.attrib['LABEL'] in ('presmaster', 'modifiedmaster'))
    print(ET.tounicode(mets, pretty_print=True))



def test_labels_in_mets_dnx_single_file():
    """Test that labels are added to generalFileCharactierists secion and
    structMap, and that they are populated with the filenames (sans extensions)"""
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

    gfc = mets.findall('.//section[@id="generalFileCharacteristics"]/record')[0]
    # since we're doing this, let's also test the FileOriginalName key
    file_original_name =  gfc.findall('./key[@id="fileOriginalName"]')[0]
    assert(file_original_name.text == 'presmaster.jpg')
    label = gfc.findall('./key[@id="label"]')[0]
    assert(label.text == 'presmaster')
    struct_map = mets.findall('./{http://www.loc.gov/METS/}structMap')[0]
    file_div = struct_map.findall('.//{http://www.loc.gov/METS/}div[@TYPE="FILE"]')[0]
    assert(file_div.attrib['LABEL'] == 'presmaster')
    # assert(gfc_file_original_name == 'presmaster.jpg')
    # print(ET.tounicode(mets, pretty_print=True))

def test_digtial_original_dnx():
    """Test that the digitalOriginal value is being properly translated
    from a boolean input to a lower-case string of 'true' or 'false'"""
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

    grc = mets.findall('.//section[@id="generalRepCharacteristics"]')[0]
    # print(ET.tounicode(grc[0], pretty_print=True))
    do = grc.findall('.//key[@id="DigitalOriginal"]')[0]
    assert (do.text == 'true')
    # for grc in general_rep_characteristics:
    #     assert(grc.text == 'true')

def test_digtial_original_dnx_single_file():
    """Test that the digitalOriginal value is being properly translated
    from a boolean input to a lower-case string of 'true' or 'false' for a
    single-file METS"""
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
        digital_original=True
        )
    grc = mets.findall('.//section[@id="generalRepCharacteristics"]')[0]
    # print(ET.tounicode(grc[0], pretty_print=True))
    do = grc.findall('.//key[@id="DigitalOriginal"]')[0]
    assert (do.text == 'true')
    # for grc in general_rep_characteristics:
    #     assert(grc.text == 'true')
    print(ET.tounicode(mets, pretty_print=True))


# 2017-08-01: Removed "ORDER" attribute, so the following test is no longer
# required
# def test_structmap_order_attrib_single_file():
#     """Test for order to be included in single file METS structmaps
#     At both div levels"""
#     ie_dc_dict = {"dc:title": "test title"}
#     mets = mdf.build_single_file_mets(
#         ie_dmd_dict=ie_dc_dict,
#         filepath=os.path.join(
#             os.path.dirname(os.path.realpath(__file__)),
#             'data',
#             'test_batch_1',
#             'pm',
#             'presmaster.jpg'),
#         generalIECharacteristics=[{
#             'submissionReason': 'bornDigitalContent',
#             'IEEntityType': 'periodicIE'}],
#         digital_original=True
#         )
#     structmap_divs = mets.findall('.//{http://www.loc.gov/METS/}structMap/{http://www.loc.gov/METS/}div')
#     for div in structmap_divs:
#         print(div.attrib["ORDER"])
#         assert("ORDER" in div.attrib.keys())
    # grc = mets.findall('.//section[@id="generalRepCharacteristics"]')[0]
    # print(ET.tounicode(grc[0], pretty_print=True))
    # do = grc.findall('.//key[@id="DigitalOriginal"]')[0]
    # assert (do.text == 'true')
    # for grc in general_rep_characteristics:
    #     assert(grc.text == 'true')
    # print(ET.tounicode(mets, pretty_print=True))


# 2017-07-20: Removed "ORDER" attribute, so the following test is no longer
# required
# def test_structmap_order_attrib():
#     """Test for order to be included in single file METS structmaps divs where TYPE="FILE" """
#     ie_dc_dict = {"dc:title": "test title"}
#     mets = mdf.build_mets(
#         ie_dmd_dict=ie_dc_dict,
#         pres_master_dir=os.path.join(
#             os.path.dirname(os.path.realpath(__file__)),
#             'data',
#             'test_batch_1',
#             'pm'),
#         modified_master_dir=os.path.join(
#             os.path.dirname(os.path.realpath(__file__)),
#             'data',
#             'test_batch_1',
#             'mm'),
#         input_dir=os.path.join(os.path.dirname(
#             os.path.realpath(__file__)),
#             'data',
#             'test_batch_1'),
#         generalIECharacteristics=[{
#             'submissionReason': 'bornDigitalContent',
#             'IEEntityType': 'periodicIE'}],
#         digital_original=True
#         )
#     print(ET.tounicode(mets, pretty_print=True))
#     structmap_divs = mets.findall('.//{http://www.loc.gov/METS/}structMap/{http://www.loc.gov/METS/}div')
#     for div in structmap_divs:
#         if "TYPE" in div.attrib and div.attrib["TYPE"] == "FILE":
#             print(div.attrib["ORDER"])
#             assert("ORDER" in div.attrib.keys())


def test_mets_dnx_with_json_supply_filesizebytes():
    """For testing new function for building SIP with JSON documents
    describing the structure and metadata of files.
    Specifically testing that all files in the filesec have an ADMID
    attrib."""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_2'),
        digital_original=True)
    print(ET.tounicode(mets, pretty_print=True))
    bytes_list = mets.findall(
        './/key[@id="fileSizeBytes"]')
    # print(bytes_list)
    for element in bytes_list:
        assert element.text in ['119191', '119192']


def test_mets_dnx_with_json_structmap_IDs():
    """Make sure that each div in the structMap gets the right ID
    a bug was found where all fptr elements in the structMap got the
    fid of the first file. This is to check that doesn't happen anymore."""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_2'),
        digital_original=True)
    fptr_list = mets.findall('.//{http://www.loc.gov/METS/}fptr')
    # print(fptr_list)
    file_ids = []
    for fptr in fptr_list:
        file_ids.append(fptr.attrib['FILEID'])
    assert len(file_ids) == len(set(file_ids))

def test_mets_dnx_with_json_structmap_IDs():
    """Make sure files are in the correct order in the
    StructMap"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"},
         {"fileOriginalName": "img3.jpg",
         "fileOriginalPath": "img3.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True)
    div_list = mets.findall('.//{http://www.loc.gov/METS/}div/{http://www.loc.gov/METS/}div//{http://www.loc.gov/METS/}div')
    # print(fptr_list)
    div_labels = []
    print(mets.tounicode(pretty_print=True))
    for div in div_list:
        div_labels.append(div.attrib['LABEL'])
    assert div_labels == ["Image One", "Image Two", "Image Three"]


def test_structmap_has_table_of_contents_div_for_json():
    """Make sure files are in the correct order in the
    StructMap"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"},
         {"fileOriginalName": "img3.jpg",
         "fileOriginalPath": "img3.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True)
    toc_div = mets.find('.//{http://www.loc.gov/METS/}structMap/{http://www.loc.gov/METS/}div/{http://www.loc.gov/METS/}div')
    # print(fptr_list)
    print(toc_div.attrib['LABEL'])
    # div_labels = []
    assert toc_div.attrib['LABEL'] == 'Table of Contents'
    # print(mets.tounicode(pretty_print=True))



def test_structmap_file_type_exists():
    """Test to make sure the TYPE="FILE" attrib exists in the
    structMap file-level divs, and that it only includes the
    filename up to the extension."""
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
    struct_maps = mets.findall('./{http://www.loc.gov/METS/}structMap')
    for struct_map in struct_maps:
        file_divs = struct_map.findall('.//{http://www.loc.gov/METS/}div[@TYPE="FILE"]')
        assert(len(file_divs) > 0)
    print(ET.tounicode(mets, pretty_print=True))


def test_structmap_has_table_of_contents_div_for_normal_factory():
    """Test to make sure the structumap has a second-layer div with the
    LABEL value of "Table of Contents"."""
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
    struct_maps = mets.findall('./{http://www.loc.gov/METS/}structMap')
    for struct_map in struct_maps:
        second_div = struct_map.find("./{http://www.loc.gov/METS/}div/{http://www.loc.gov/METS/}div")
        print(second_div.attrib["LABEL"])
        assert(second_div.attrib["LABEL"] == "Table of Contents")
    # print(ET.tounicode(mets, pretty_print=True))


def test_structmap_has_table_of_contents_div_for_single_file_mets():
    """Test to make sure the structMap has a second-layer div with the LABEL
    value of "Table of Contents" for single_file METS."""
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

    struct_maps = mets.findall('./{http://www.loc.gov/METS/}structMap')
    for struct_map in struct_maps:
        second_div = struct_map.find("./{http://www.loc.gov/METS/}div/{http://www.loc.gov/METS/}div")
        print(second_div.attrib["LABEL"])
        assert(second_div.attrib["LABEL"] == "Table of Contents")


def test_mm_and_ad_for_json_mets():
    """Make sure that all details for mms and ads are being processed correctly"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "presmaster.jpg",
         "fileOriginalPath": "pm/presmaster.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"}]"""
    mm_json = """[{"fileOriginalName": "modifiedmaster.jpg",
         "fileOriginalPath": "mm/modifiedmaster.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"}]"""
    ad_json = """[{"fileOriginalName": "deriv.jpg",
         "fileOriginalPath": "ad/deriv.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119192"},
         {"fileOriginalName": "deriv_2.jpg",
         "fileOriginalPath": "ad/deriv_2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        modified_master_json = mm_json,
        access_derivative_json = ad_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True)
    # structmaps = mets.findall('./{http://www.loc.gov/METS/}structMap')
    assert mets.find('./{http://www.loc.gov/METS/}structMap[@ID="rep1-1"]') != None
    assert mets.find('./{http://www.loc.gov/METS/}structMap[@ID="rep2-1"]') != None
    assert mets.find('./{http://www.loc.gov/METS/}structMap[@ID="rep3-1"]') != None
    # print(ET.tounicode(mets, pretty_print=True))


def test_windows_paths_on_json_mets():
    """Make sure that all details for mms and ads are being processed correctly"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "presmaster.jpg",
         "fileOriginalPath": "pm\\\\presmaster.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"}]"""
    mm_json = """[{"fileOriginalName": "modifiedmaster.jpg",
         "fileOriginalPath": "mm\\\\modifiedmaster.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119192"}]"""
    ad_json = """[{"fileOriginalName": "deriv.jpg",
         "fileOriginalPath": "ad\\\\deriv.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119192"},
         {"fileOriginalName": "deriv_2.jpg",
         "fileOriginalPath": "ad\\\\deriv_2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Four",
         "note": "This is a note for image 4",
         "fileSizeBytes": "119192"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json=pm_json,
        modified_master_json=mm_json,
        access_derivative_json=ad_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True)
    for flocat in mets.findall('.//{http://www.loc.gov/METS/}FLocat'):
        href = '{http://www.w3.org/1999/xlink}href'
        print(flocat.attrib[href])
        assert('\\' not in flocat.attrib[href])


def test_logical_structmap_gets_labelled_logical():
    """Make sure the default "PHYSICAL" label gets overwritten"""
    ie_dc_dict = [{'dc:title': 'Test deposit'}]
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        digital_original=True)
    print(ET.tounicode(mets, pretty_print=True))
    assert (mets.find("{http://www.loc.gov/METS/}structMap"
                      ).attrib['TYPE'] == 'LOGICAL')

    third_tier = mets.findall("{http://www.loc.gov/METS/}structMap/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div")

    for div in third_tier:
        child = div.getchildren()[0]
        assert(child.tag in ["{http://www.loc.gov/METS/}fptr",
                             "{http://www.loc.gov/METS/}div"])


def test_multi_dimension_structmap_gets_flattened():
    """Multi-level structmaps get flattened when structmap type is selected."""
    ie_dc_dict = [{'dc:title': 'Test deposit'}]
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        digital_original=True,
        structmap_type='PHYSICAL')
    print(ET.tounicode(mets, pretty_print=True))
    assert (mets.find("{http://www.loc.gov/METS/}structMap"
                      ).attrib['TYPE'] == 'PHYSICAL')
    third_tier = mets.findall("{http://www.loc.gov/METS/}structMap/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div")
    for div in third_tier:
        child = div.getchildren()[0]
        assert(child.tag == "{http://www.loc.gov/METS/}fptr")

def test_multi_dim_sm_gets_phys_and_log():
    """Multi-level structmaps get both SM types when "BOTH" is selected"""
    ie_dc_dict = [{'dc:title': 'Test deposit'}]
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        digital_original=True,
        structmap_type='BOTH')
    print(ET.tounicode(mets, pretty_print=True))
    structmaps = mets.findall("{http://www.loc.gov/METS/}structMap")
    logical_checked = False
    physical_checked = False
    for structmap in structmaps:
        print(structmap.attrib['TYPE'])
        if structmap.attrib['TYPE'].upper() == 'PHYSICAL':
            physical_checked = True
        if structmap.attrib['TYPE'].upper() == 'LOGICAL':
            logical_checked = True
        fptrs = structmap.findall(".//{http://www.loc.gov/METS/}fptr")
        assert(len(fptrs) > 1)
    assert physical_checked == True
    assert logical_checked == True


def test_logical_structmap_gets_labelled_logical_with_bad_flags():
    """SM "PHYSICAL" label still gets overwritten if structmap_type is a random word"""
    ie_dc_dict = [{'dc:title': 'Test deposit'}]
    mets = mdf.build_mets(
        ie_dmd_dict=ie_dc_dict,
        pres_master_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_5'),
        digital_original=True,
        structmap_type="hAMBuRGERS")
    # print(ET.tounicode(mets, pretty_print=True))
    assert (mets.find("{http://www.loc.gov/METS/}structMap"
                      ).attrib['TYPE'] == 'LOGICAL')

    third_tier = mets.findall("{http://www.loc.gov/METS/}structMap/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div/" +
                              "{http://www.loc.gov/METS/}div")

    for div in third_tier:
        child = div.getchildren()[0]
        assert(child.tag in ["{http://www.loc.gov/METS/}fptr",
                             "{http://www.loc.gov/METS/}div"])


def test_structmap_for_json_mets_default():
    """Make sure that the default hierarchical structmap is type "LOGICAL" """
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img3.jpg",
         "fileOriginalPath": "path/to/other/files/img3.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img4.jpg",
         "fileOriginalPath": "path/to/other/files/img4.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Four",
         "note": "This is a note for image 4",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img5.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img5.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Five",
         "note": "This is a note for image 5",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img6.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img6.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Six",
         "note": "This is a note for image 6",
         "fileSizeBytes": "119191"}
         ]"""

    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json=pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True)
    toc_div = mets.find('.//{http://www.loc.gov/METS/}structMap/{http://www.loc.gov/METS/}div/{http://www.loc.gov/METS/}div')
    # print(fptr_list)
    print(toc_div.attrib['LABEL'])
    # div_labels = []
    assert toc_div.attrib['LABEL'] == 'Table of Contents'
    assert(mets.find(
        './/{http://www.loc.gov/METS/}structMap').attrib['TYPE'] == 'LOGICAL')


def test_structmap_for_json_mets_physical():
    """Make sure that the strucmap type is set to "PHYSICAL" when flagged"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img3.jpg",
         "fileOriginalPath": "path/to/other/files/img3.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img4.jpg",
         "fileOriginalPath": "path/to/other/files/img4.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Four",
         "note": "This is a note for image 4",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img5.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img5.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Five",
         "note": "This is a note for image 5",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img6.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img6.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Six",
         "note": "This is a note for image 6",
         "fileSizeBytes": "119191"}
         ]"""

    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json=pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True,
        structmap_type="PHYSICAL")
    assert(mets.find(
        './/{http://www.loc.gov/METS/}structMap').attrib['TYPE'] == 'PHYSICAL')
    # print(ET.tounicode(mets, pretty_print=True))

def test_structmap_for_json_mets_both():
    """Make sure that METS gets both PHYSICAL and LOGICAL SMs when flagged"""
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image One",
         "note": "This is a note for image 1",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Two",
         "note": "This is a note for image 2",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img3.jpg",
         "fileOriginalPath": "path/to/other/files/img3.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Three",
         "note": "This is a note for image 3",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img4.jpg",
         "fileOriginalPath": "path/to/other/files/img4.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Four",
         "note": "This is a note for image 4",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img5.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img5.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Five",
         "note": "This is a note for image 5",
         "fileSizeBytes": "119191"},

         {"fileOriginalName": "img6.jpg",
         "fileOriginalPath": "path/to/yet/more/files/img6.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image Six",
         "note": "This is a note for image 6",
         "fileSizeBytes": "119191"}
         ]"""

    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json=pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_3'),
        digital_original=True,
        structmap_type="BOTH")
    structmaps = mets.findall("{http://www.loc.gov/METS/}structMap")
    # print(structmaps)
    assert(len(structmaps) == 2)
    physical_checked = False
    logical_checked = False
    for structmap in structmaps:
        print(structmap.attrib['TYPE'])
        if structmap.attrib['TYPE'].upper() == 'PHYSICAL':
            physical_checked = True
        if structmap.attrib['TYPE'].upper() == 'LOGICAL':
            logical_checked = True
        fptrs = structmap.findall(".//{http://www.loc.gov/METS/}fptr")
        assert(len(fptrs) > 1)
    assert(physical_checked == True)
    assert(logical_checked == True)
    print(ET.tounicode(mets, pretty_print=True))


def test_mets_dnx_with_json_for_file_label():
    """File labels don't get truncated if they have periods in them
    """
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image.One",
         "note": "This is a note for image 1"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image.Two",
         "note": "This is a note for image 2"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_2'),
        digital_original=True)
    print(ET.tounicode(mets, pretty_print=True))
    file_labels_list = mets.findall('.//key[@id="label"]')
    for file_label in file_labels_list:
        print(file_label.text)
        assert file_label.text in ('Image.One', 'Image.Two')
        assert file_label.text not in ('Image',)


def test_mets_dnx_with_json_for_sm_label_with_period():
    """Structmap file labels will contain the full label, even if it has a period
    """
    ie_dc_dict = {"dc:title": "test title"}

    pm_json = """[
        {"fileOriginalName": "img1.jpg",
         "fileOriginalPath": "path/to/files/img1.jpg",
         "MD5": "aff64bf1391ac627edb3234a422f9a77",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image.One",
         "note": "This is a note for image 1"},
         {"fileOriginalName": "img2.jpg",
         "fileOriginalPath": "path/to/files/img2.jpg",
         "MD5": "9d09f20ab8e37e5d32cdd1508b49f0a9",
         "fileCreationDate": "1st of January, 1601",
         "fileModificationDate": "1st of January, 1601",
         "label": "Image.Two",
         "note": "This is a note for image 2"}
    ]"""
    mets = mdf.build_mets_from_json(
        ie_dmd_dict=ie_dc_dict,
        pres_master_json = pm_json,
        input_dir=os.path.join(CURRENT_DIR, 'data', 'test_batch_2'),
        digital_original=True)
    print(ET.tounicode(mets, pretty_print=True))
    sm_labels_list = mets.findall('.//{http://www.loc.gov/METS/}div[@TYPE="FILE"]')
    for sm_label in sm_labels_list:
        print(sm_label.attrib['LABEL'])
        assert(sm_label.attrib['LABEL'] in ('Image.One', 'Image.Two'))


def test_mets_dnx_with_pm_and_ad_for_phys_structmap_labels():
    """Make sure the correct rep labels are used.
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
        digital_original=True,
        structmap_type='PHYSICAL'
        )
    print(ET.tounicode(mets, pretty_print=True))
    mm_structmap_label = mets.find(
            '{http://www.loc.gov/METS/}structMap[@ID="rep2-1"]/' +
            '{http://www.loc.gov/METS/}div').attrib['LABEL']
    print(mm_structmap_label)
    assert(mm_structmap_label == "Modified Master")

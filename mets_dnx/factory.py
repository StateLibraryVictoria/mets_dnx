import hashlib
import json
import os
import re
import time

from lxml import etree as ET

from pydc import factory as dc_factory
from pymets import mets_factory as mf
from pymets import mets_model as mm
from pydnx import factory as dnx_factory

def generate_md5(filepath, block_size=2**20):
    """For producing md5 checksums for a file at a specified filepath."""
    m = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def build_amdsec(amdsec, tech_sec=None, rights_sec=None, 
                 source_sec=None, digiprov_sec=None):
    amd_id = amdsec.attrib['ID']
    amd_tech = ET.SubElement(
                    amdsec, 
                    "{http://www.loc.gov/METS/}techMD", 
                    ID=amd_id + "-tech")
    amd_rights = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}rightsMD",
                    ID=amd_id + "-rights")
    amd_source = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}sourceMD",
                    ID=amd_id + "-source")
    amd_digiprov = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}digiprovMD",
                    ID=amd_id + "-digiprov")

    for el in [amd_tech, amd_rights, amd_source, amd_digiprov]:
        mdWrap = ET.SubElement(
                        el, 
                        "{http://www.loc.gov/METS/}mdWrap",
                        MDTYPE="OTHER", OTHERMDTYPE="dnx")
        xmlData = ET.SubElement(mdWrap, "{http://www.loc.gov/METS/}xmlData")
        if (el.tag == "{http://www.loc.gov/METS/}techMD" and 
                tech_sec != None):
            xmlData.append(tech_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}techMD" and 
                tech_sec == None):
            xmlData.append(ET.Element("dnx",
                xmlns="http://www.exlibrisgroup.com/dps/dnx"))

        if (el.tag == "{http://www.loc.gov/METS/}rightsMD" and 
                rights_sec != None):
            xmlData.append(rights_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}rightsMD" and 
                rights_sec == None):
            xmlData.append(ET.Element("dnx",
                xmlns="http://www.exlibrisgroup.com/dps/dnx"))

        if (el.tag == "{http://www.loc.gov/METS/}sourceMD" and 
                source_sec != None):
            xmlData.append(source_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}sourceMD" and 
                source_sec == None):
            xmlData.append(ET.Element("dnx",
                xmlns="http://www.exlibrisgroup.com/dps/dnx"))

        if (el.tag == "{http://www.loc.gov/METS/}digiprovMD" and 
                digiprov_sec != None):
            xmlData.append(digiprov_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}digiprovMD" and 
                digiprov_sec == None):
            xmlData.append(ET.Element("dnx",
                xmlns="http://www.exlibrisgroup.com/dps/dnx"))


def _build_ie_dmd_amd(mets,
                   ie_dmd_dict=None,
                   generalIECharacteristics=None,
                   cms=None,
                   webHarvesting=None,
                   objectIdentifier=None,
                   accessRightsPolicy=None,
                   eventList=None):
    # first off, build ie-dmdsec
    # check if ie_dmd_dict is a single dictionary inside a list
    # (which is the convention for the METS factory, but not necessary for
    # the DC Factory)
    if type(ie_dmd_dict) == list and len(ie_dmd_dict) == 1:
        ie_dmd_dict = ie_dmd_dict[0]
    dc_record = dc_factory.build_dc_record(ie_dmd_dict)
    dmdsec = ET.SubElement(
                mets,
                "{http://www.loc.gov/METS/}dmdSec",
                ID="ie-dmd")
    mdwrap = ET.SubElement(
                dmdsec,
                "{http://www.loc.gov/METS/}mdWrap",
                MDTYPE="DC")
    xmldata = ET.SubElement(
                mdwrap,
                "{http://www.loc.gov/METS/}xmlData")
    xmldata.append(dc_record)

    # build ie amd section
    ie_amdsec = ET.SubElement(
                    mets,
                    "{http://www.loc.gov/METS/}amdSec",
                    ID="ie-amd")
    if ((generalIECharacteristics != None) 
            or (cms != None) 
            or (objectIdentifier != None)
            or (webHarvesting != None)):
        ie_amd_tech = dnx_factory.build_ie_amdTech(
            generalIECharacteristics=generalIECharacteristics,
            objectIdentifier=objectIdentifier,
            CMS=cms,
            webHarvesting=webHarvesting)
    else:
        ie_amd_tech = None
    if (accessRightsPolicy != None):
        ie_amd_rights = dnx_factory.build_ie_amdRights(
            accessRightsPolicy=accessRightsPolicy)
    else:
        ie_amd_rights = None
    if (eventList != None):
        ie_amd_digiprov = dnx_factory.build_ie_amdDigiprov(event=eventList)
    else:
        ie_amd_digiprov = None
    # TODO (2016-10-03): add functionality for ie_amdSourceMD
    ie_amd_source = None
    build_amdsec(
            ie_amdsec,
            ie_amd_tech,
            ie_amd_rights,
            ie_amd_digiprov,
            ie_amd_source)

def build_mets(ie_dmd_dict=None,
                pres_master_dir=None, 
                modified_master_dir=None,
                access_derivative_dir=None,
                cms=None,
                webHarvesting=None,
                generalIECharacteristics=None,
                objectIdentifier=None,
                accessRightsPolicy=None,
                eventList=None,
                input_dir=None,
                digital_original=False):

    mets = mf.build_mets()

    _build_ie_dmd_amd(mets,
            ie_dmd_dict=ie_dmd_dict,
            generalIECharacteristics=generalIECharacteristics,
            cms=cms,
            webHarvesting=webHarvesting,
            objectIdentifier=objectIdentifier,
            accessRightsPolicy=accessRightsPolicy,
            eventList=eventList)

    mf.build_amdsec_filegrp_structmap(
        mets,
        ie_id="ie1", 
        pres_master_dir=pres_master_dir,
        modified_master_dir=modified_master_dir,
        access_derivative_dir=access_derivative_dir,
        digital_original=digital_original,
        input_dir=input_dir)


    # Create representation_level and file_level amdsecs, based on
    # the filegrp details
    file_groups = mets.findall('.//{http://www.loc.gov/METS/}fileGrp')
    for file_group in file_groups:
        rep_id = file_group.attrib['ID']
        rep_type = mets.find('.//{%s}structMap[@ID="%s-1"]/{%s}div' % 
            ('http://www.loc.gov/METS/', rep_id, 'http://www.loc.gov/METS/')
            ).attrib['LABEL']
        
        if rep_type == 'Preservation Master':
            pres_type = 'PRESERVATION_MASTER'
            pres_location = pres_master_dir
        elif rep_type == 'Modified Master':
            pres_type = 'MODIFIED_MASTER'
            pres_location = modified_master_dir
        elif rep_type == 'Access Derivative':
            pres_location = access_derivative_dir
            pres_type = 'ACCESS_DERIVATIVE'
        else:
            pres_type = None
            pres_location = '.'

        rep_amdsec = mets.xpath("//mets:amdSec[@ID='%s']" % 
                str(rep_id + '-amd'), namespaces=mets.nsmap)[0]
        general_rep_characteristics = [{'RevisionNumber': '1', 
                'DigitalOriginal': str(digital_original).lower(),
                'usageType': 'VIEW',
                'preservationType': pres_type}]
        rep_amd_tech = dnx_factory.build_rep_amdTech(
            generalRepCharacteristics=general_rep_characteristics)
        rep_amd_rights = None
        rep_amd_digiprov = None
        rep_amd_source = None
        build_amdsec(
            rep_amdsec,
            tech_sec=rep_amd_tech, 
            rights_sec=rep_amd_rights,
            source_sec=rep_amd_source, 
            digiprov_sec=rep_amd_digiprov)

        # create amdsec for files
        for fl in file_group.findall('./{http://www.loc.gov/METS/}file'):
            fl_id = fl.attrib['ID']
            fl_amdsec = None
            fl_amdsec = mets.xpath("//mets:amdSec[@ID='%s']" % 
                    str(fl_id + '-amd'), namespaces=mets.nsmap)[0]
            file_original_location = os.path.join(input_dir,
                fl.find('./{http://www.loc.gov/METS/}FLocat').attrib[
                        '{http://www.w3.org/1999/xlink}href'])
            file_size_bytes = os.path.getsize(file_original_location)
            last_modified = time.strftime(
                    "%Y-%m-%dT%H:%M:%S",
                    time.localtime(os.path.getmtime(file_original_location)))
            created_time = time.strftime(
                    "%Y-%m-%dT%H:%M:%S",
                    time.localtime(os.path.getctime(file_original_location)))
            general_file_characteristics = [{
                'fileOriginalPath': file_original_location,
                'fileSizeBytes': str(file_size_bytes),
                'fileModificationDate': last_modified,
                'fileCreationDate': created_time}]

            file_fixity =  [{
                'fixityType': 'MD5',
                'fixityValue': generate_md5(file_original_location)}]

            fl_amd_tech = dnx_factory.build_file_amdTech(
                generalFileCharacteristics=general_file_characteristics,
                fileFixity=file_fixity)
            build_amdsec(fl_amdsec, tech_sec=fl_amd_tech)


    # clean up identifiers so they are consistent with Rosetta requirements
    for element in mets.xpath(".//*[@ID]"):
        element.attrib['ID'] = re.sub('ie[0-9]+\-', '', element.attrib['ID'])
        element.attrib['ID'] = re.sub(
                'rep([0-9]+)\-file([0-9]+)',
                r'fid\2-\1',
                element.attrib['ID'])
    for element in mets.xpath(".//*[@ADMID]"):
        element.attrib['ADMID'] = re.sub(
                'ie[0-9]+\-rep([0-9]+)\-file([0-9]+)-amd',
                r'fid\2-\1-amd',
                element.attrib['ADMID'])
        element.attrib['ADMID'] = re.sub(
                'ie[0-9]+\-rep([0-9]+)-amd',
                r'rep\1-amd',
                element.attrib['ADMID'])
    for element in mets.xpath(".//*[@FILEID]"):
        element.attrib['FILEID'] = re.sub(
                'ie[0-9]+\-rep([0-9])+\-file([0-9]+)',
                r'fid\2-\1',
                element.attrib['FILEID'])
    return mets


def build_single_file_mets(ie_dmd_dict=None,
                filepath=None,
                cms=None,
                webHarvesting=None,
                generalIECharacteristics=None,
                objectIdentifier=None,
                accessRightsPolicy=None,
                eventList=None,
                digital_original=False):
    mets = mf.build_mets()
    _build_ie_dmd_amd(mets,
            ie_dmd_dict=ie_dmd_dict,
            generalIECharacteristics=generalIECharacteristics,
            cms=cms,
            webHarvesting=webHarvesting,
            objectIdentifier=objectIdentifier,
            accessRightsPolicy=accessRightsPolicy,
            eventList=eventList)

    # Build rep amdsec
    rep_amdsec = ET.Element("{http://www.loc.gov/METS/}amdSec", ID="rep1-amd")
    general_rep_characteristics = [{'RevisionNumber': '1', 
            'DigitalOriginal': str(digital_original).lower(),
            'usageType': 'VIEW',
            'preservationType': 'PRESERVATION_MASTER'}]
    rep_amd_tech = dnx_factory.build_rep_amdTech(
        generalRepCharacteristics=general_rep_characteristics)
    rep_amd_rights = None
    rep_amd_digiprov = None
    rep_amd_source = None
    build_amdsec(
        rep_amdsec,
        tech_sec=rep_amd_tech, 
        rights_sec=rep_amd_rights,
        source_sec=rep_amd_source, 
        digiprov_sec=rep_amd_digiprov)
    mets.append(rep_amdsec)

    # Build file amdsec
    fl_amdsec = ET.Element("{http://www.loc.gov/METS/}amdSec", ID="fid1-1-amd")
    file_original_location = filepath
    file_size_bytes = os.path.getsize(file_original_location)
    last_modified = time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.localtime(os.path.getmtime(file_original_location)))
    created_time = time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.localtime(os.path.getctime(file_original_location)))
    general_file_characteristics = [{
        'fileOriginalPath': file_original_location,
        'fileSizeBytes': str(file_size_bytes),
        'fileModificationDate': last_modified,
        'fileCreationDate': created_time}]

    file_fixity =  [{
        'fixityType': 'MD5',
        'fixityValue': generate_md5(file_original_location)}]

    fl_amd_tech = dnx_factory.build_file_amdTech(
        generalFileCharacteristics=general_file_characteristics,
        fileFixity=file_fixity)
    build_amdsec(fl_amdsec, tech_sec=fl_amd_tech)
    mets.append(fl_amdsec)

    # build filesec
    filename = os.path.basename(filepath)
    filesec = mm.FileSec()
    filegrp = mm.FileGrp(ID="rep1", ADMID="rep1-amd", USE="VIEW")
    filesec.append(filegrp)

    file_el = mm.File(ID='fid1-1', ADMID="fid1-1-amd")
    filegrp.append(file_el)

    flocat = mm.FLocat(LOCTYPE="URL", href=filename)
    file_el.append(flocat)

    mets.append(filesec)
    
    # build structmap
    structmap = mm.StructMap(ID="rep1-1", TYPE="PHYSICAL")

    div_1 = mm.Div(LABEL="Preservation Master")
    structmap.append(div_1)

    div_2 = mm.Div(TYPE="FILE", LABEL=filename)
    div_1.append(div_2)

    fptr = mm.Fptr(FILEID='fid1-1')
    div_2.append(fptr)

    mets.append(structmap)

    return mets

def _build_fl_amd_from_json(mets, file_no, rep_no, item, path):
    fl_amd_sec = mm.AmdSec(ID="fid{}-{}".format(file_no, rep_no))
    fileOriginalName = None
    fileSizeBytes = None
    md5sum = None
    fileCreationDate = None
    fileModificationDate = None
    note = None
    # events = None

    gfc = {} # general file characteristics
    fixity = {}
    events = {}
    if path != None:
        gfc['fileOriginalPath'] = os.path.join(path, item["name"])
    else:
        gfc['fileOriginalPath'] = item["name"]
    for key in item.keys():
        if key == 'name':
            gfc['fileOriginalName'] = item[key]
        if key == 'fileSizeBytes':
            gfc['fileSizeBytes'] = item[key]
        if key == 'fileCreationDate':
            gfc['fileCreationDate'] = item[key]
        if key == 'fileModificationDate':
            gfc['fileModificationDate'] = item[key]
        if key == 'note':
            gfc['note'] = item[key]

        # fixity values
        if key.upper() == 'MD5':
            fixity['fixityType'] = 'MD5'
            fixity['fixityValue'] = item[key]
        # provenance values
        if key == 'events':
            events = item[key]

    # Check the supplied fixity to make sure it can be reproduced
    fileSizeBytes = None
    if md5sum and fileOriginalpath:
        fileSizeBytes = os.path.getsize(fileOriginalpath)
        checksum = generate_md5(fileOriginalpath)
        if md5sum != checksum:
            raise ValueError("could not reproduce MD5 sum for {}: Expected {}, got {}".format(
                fileOriginalPath, md5sum, checksum))

    # reset any empty dicts to None value
    if len(gfc) == 0:
        gfc = None
    if len(fixity) == 0:
        fixity = None
    if len(events) == 0:
        events = None

    fl_amd_tech = dnx_factory.build_file_amdTech(
        generalFileCharacteristics=[gfc],
        fileFixity=[fixity])
    fl_amd_digiprov = dnx_factory.build_ie_amdDigiprov(
        event=events) # yes, the call to ie amdDigiprov is intentional,
    # as we don't yet have a file digiprov builder. Should be fine though.

    build_amdsec(fl_amd_sec, tech_sec=fl_amd_tech, digiprov_sec=fl_amd_digiprov)
    mets.append(fl_amd_sec)


    fileSizeBytes = None
    if md5sum and fileOriginalpath:
        fileSizeBytes = os.path.getsize(fileOriginalpath)
        checksum = generate_md5(fileOriginalpath)
        if md5sum != checksum:
            raise ValueError("could not reproduce MD5 sum for {}: Expected {}, got {}".format(
                fileOriginalPath, md5sum, checksum))


def _parse_json(mets, rep_no, json_doc, path=None):
    if type(json_doc) == str:
        rep_dict = json.loads(json_doc)
    else:
        rep_dict = json_doc
    file_no = 1
    for item in rep_dict:
        try:
            if item['type'] == 'file':
                _build_fl_amd_from_json(mets, file_no, rep_no, item, path)
                # Add file number to assist with filesec construction
                item['file_no'] = file_no
                file_no += 1
            elif item['type'] == 'directory':
                if path == None:
                    path = os.path.join(item['name'])
                else:
                    path = os.path.join(path, item['name'])
                _parse_json(mets, rep_no, item['children'], path)
            else:
                raise ValueError("This item does not have a valid type value: {}".format(item))
        except KeyError:
            print("The following json does not have a 'type' value: {}".format(item))


def _parse_json_for_filegrp(filegrp, rep_no, json_doc, input_dir, path=None):
    if type(json_doc) == str:
        rep_dict = json.loads(json_doc)
    else:
        rep_dict = json_doc
    file_no = 1
    for item in rep_dict:
        try:
            if item['type'] == 'file':
                # 2016-10-27: Hacky way of getting relative file location
                # Simply shaving the input_dir off the front of the full path 
                href = os.path.join(path, item['name'])[len(input_dir) + 1:]
                file_el = mm.File(ID="fid{}-{}".format(file_no, rep_no))
                flocat = mm.FLocat(LOCTYPE="URL", href=href)
                file_el.append(flocat)
                filegrp.append(file_el)
                file_no += 1
            elif item['type'] == 'directory':
                if path == None:
                    path = os.path.join(item['name'])
                else:
                    path = os.path.join(path, item['name'])
                _parse_json_for_filegrp(filegrp, rep_no, item['children'], input_dir, path)
            else:
                raise ValueError("This item does not have a valid type value: {}".format(item))
        except KeyError:
            print("The following json does not have a 'type' value: {}".format(item))


def _parse_json_for_structmap(div, rep_no, json_doc, path=None):
    if type(json_doc) == str:
        rep_dict = json.loads(json_doc)
    else:
        rep_dict = json_doc
    file_no = 1
    for item in rep_dict:
        try:
            if item['type'] == 'file':
                # _build_fl_amd_from_json(mets, file_no, rep_no, item, path)
                if 'label' in item.keys():
                    label = item['label']
                else:
                    label = item['name']
                div2 = mm.Div(TYPE="FILE", LABEL=label)
                div.append(div2)

                fptr = mm.Fptr(FILEID="fid{}-{}".format(file_no, rep_no))
                div2.append(fptr)
                
                file_no += 1
            elif item['type'] == 'directory':
                if path == None:
                    path = os.path.join(item['name'])
                    div2 = mm.Div(TYPE="FOLDER", LABEL=item['name'])
                else:
                    path = os.path.join(path, item['name'])
                    div2 = mm.Div(TYPE="FOLDER", LABEL=item['name'])
                div.append(div2)
                _parse_json_for_structmap(div2, rep_no, item['children'], path)
            else:
                raise ValueError("This item does not have a valid type value: {}".format(item))
        except KeyError:
            print("The following json does not have a 'type' value: {}".format(item))


def _build_rep_amdsec(mets, rep_no, digital_original, preservation_type):
    rep_amdsec = ET.Element("{http://www.loc.gov/METS/}amdSec", ID="rep{}-amd".format(rep_no))
    general_rep_characteristics = [{'RevisionNumber': '1', 
            'DigitalOriginal': str(digital_original).lower(),
            'usageType': 'VIEW',
            'preservationType': preservation_type}]
    rep_amd_tech = dnx_factory.build_rep_amdTech(
        generalRepCharacteristics=general_rep_characteristics)
    rep_amd_rights = None
    rep_amd_digiprov = None
    rep_amd_source = None
    build_amdsec(
        rep_amdsec,
        tech_sec=rep_amd_tech, 
        rights_sec=rep_amd_rights,
        source_sec=rep_amd_source, 
        digiprov_sec=rep_amd_digiprov)
    mets.append(rep_amdsec)

def build_sip_from_json(ie_dmd_dict=None,
                pres_master_json=None, 
                modified_master_json=None,
                access_derivative_json=None,
                cms=None,
                webHarvesting=None,
                generalIECharacteristics=None,
                objectIdentifier=None,
                accessRightsPolicy=None,
                eventList=None,
                input_dir=None,
                digital_original=False):
    """Build a METS XML file using JSON-formatted data describing the 
    rep structures, rather than directory paths."""
    mets = mf.build_mets()
    _build_ie_dmd_amd(mets,
        ie_dmd_dict=ie_dmd_dict,
        generalIECharacteristics=generalIECharacteristics,
        cms=cms,
        webHarvesting=webHarvesting,
        objectIdentifier=objectIdentifier,
        accessRightsPolicy=accessRightsPolicy,
        eventList=eventList)

    rep_no = 1
    if pres_master_json != None:
        pmd = json.loads(pres_master_json)
        pm_rep_no = rep_no
        # Build rep AMD Sec
        _build_rep_amdsec(mets, rep_no, digital_original, 'PRESERVATION_MASTER')
        # run through json structure and find files, assembling their
        # filepaths along the way
        _parse_json(mets, rep_no, pres_master_json)
        rep_no += 1
    if modified_master_json != None:
        mm_rep_no = rep_no
        mmd = json.loads(modified_master_json)
        _build_rep_amdsec(mets, rep_no, digital_original, 'MODIFIED_MASTER')
        # _build_fl_amd_from_json(mets, rep_no, modified_master_json)
        _parse_json(mets, rep_no, modified_master_json)
        rep_no += 1
    if access_derivative_json != None:
        add = json.loads(access_derivative_json)
        ad_rep_no = rep_no
        _build_rep_amdsec(mets, rep_no, digital_original, 'ACCESS_DERIVATIVE')
        # _build_fl_amd_from_json(mets, rep_no, access_derivative_json)
        _parse_json(mets, rep_no, access_derivative_json)
        rep_no += 1

    # build filesec
    # print(pres_master_json)
    filesec = mm.FileSec()
    if pres_master_json != None:
        # print("found presmasterdir")
        filegrp = mm.FileGrp(ID="rep{}".format(pm_rep_no),
                    ADMID="rep{}-amd".format(pm_rep_no))
        _parse_json_for_filegrp(filegrp, pm_rep_no, pres_master_json, input_dir)
        filesec.append(filegrp)
    if modified_master_json != None:
        filegrp = mm.FileGrp(ID="rep{}".format(mm_rep_no),
                    ADMID="rep{}-amd".format(mm_rep_no))
        _parse_json_for_filegrp(filegrp, mm_rep_no, modified_master_json, input_dir)
        filesec.append(filegrp)
    if access_derivative_json != None:
        filegrp = mm.FileGrp(ID="rep{}".format(ad_rep_no),
                    ADMID="rep{}-amd".format(ad_rep_no))
        _parse_json_for_filegrp(filegrp, ad_rep_no, modified_master_json, input_dir)
        filesec.append(filegrp)


    mets.append(filesec)


    # build structmaps
    structmap = mm.StructMap(ID="rep{}-1".format(rep_no), TYPE="PHYSICAL")
    if pres_master_json != None:
        div1 = mm.Div(LABEL='Preservation Master')
        structmap.append(div1)
        mets.append(structmap)
        _parse_json_for_structmap(div1, pm_rep_no, pres_master_json)
    if modified_master_json != None:
        div1 = mm.Div(LABEL='Modified Master')
        structmap.append(div1)
        mets.append(structmap)
        _parse_json_for_structmap(div1, mm_rep_no, modified_master_json)
    if access_derivative_json != None:
        div1 = mm.Div(LABEL='Access Derivative')
        structmap.append(div1)
        mets.append(structmap)
        _parse_json_for_structmap(div1, ad_rep_no, access_derivative_json)

    return mets

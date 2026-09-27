import pydicom

def anonymize_dicom_header(dcm_path):
    """
    Reads a raw clinical DICOM file and scrubs Protected Health Information (PHI)
    to enforce strict data compliance routines.
    """
    dcm = pydicom.dcmread(dcm_path)
    
    # Overwrite identifying metadata strings with secure, anonymous research tokens
    dcm.PatientName = "ANONYMOUS^RESEARCH^SUBJECT"
    dcm.PatientID = "SUBJ_ID_99482_SECURE"
    dcm.InstitutionName = "CLEANED_RESEARCH_SITE_A"
    
    if 'PatientBirthDate' in dcm: dcm.PatientBirthDate = ""
    return dcm

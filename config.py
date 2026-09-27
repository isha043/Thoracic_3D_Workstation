# ==============================================================================
# 🔬 RESEARCH USE ONLY (RUO) REGULATORY CONFIGURATION MODULE
# ==============================================================================
class MedicalDeviceConfig:
    def __init__(self, mode="RESEARCH"):
        self.current_mode = mode.upper()
        self.software_version = "v1.0.4-RUO"
        
        if self.current_mode == "CLINICAL":
            self.fda_approved_mode = True
            self.hipaa_encryption_active = True
            self.audit_logging_strict = True
            self.product_label = "Diagnostic Software as a Medical Device (SaMD)"
        else:
            self.fda_approved_mode = False
            self.hipaa_encryption_active = False
            self.audit_logging_strict = False
            self.product_label = "FOR RESEARCH USE ONLY (RUO). NOT FOR CLINICAL DIAGNOSTIC USE."

    def print_system_status(self):
        print("="*65)
        print(f"🧬 MEDICAL ASSET ARCHITECTURE PIPELINE - CORE CONFIG")
        print("="*65)
        print(f"Current System State:  [{self.current_mode} MODE]")
        print(f"Software Version:      {self.software_version}")
        print(f"Legal Product Label:   {self.product_label}")
        print("="*65)

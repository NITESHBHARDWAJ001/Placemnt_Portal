from app.validators.eligibility_validators import check_eligibility


class EligibilityService:
    @staticmethod
    def evaluate(student_profile, drive):
        is_eligible, reasons = check_eligibility(student_profile, drive)
        return {"eligible": is_eligible, "reasons": reasons}

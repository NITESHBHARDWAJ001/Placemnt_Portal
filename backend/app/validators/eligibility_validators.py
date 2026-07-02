def check_eligibility(student_profile, drive) -> tuple[bool, list[str]]:
    reasons = []

    if student_profile.cgpa is None or student_profile.cgpa < (drive.min_cgpa or 0):
        reasons.append(f"Requires minimum CGPA of {drive.min_cgpa}")

    if (student_profile.backlog_count or 0) > (drive.max_backlogs or 0):
        reasons.append(f"Allows a maximum of {drive.max_backlogs} backlog(s)")

    branches = drive.branches_list()
    if branches and student_profile.branch not in branches:
        reasons.append(f"Open only to branches: {', '.join(branches)}")

    if drive.eligible_batch and student_profile.batch_year != drive.eligible_batch:
        reasons.append(f"Open only to batch {drive.eligible_batch}")

    return (len(reasons) == 0, reasons)

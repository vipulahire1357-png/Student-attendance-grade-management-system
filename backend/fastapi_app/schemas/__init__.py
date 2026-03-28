"""Schemas package."""
from .student_schema import StudentSignup, StudentProfile, StudentUpdate, ProjectCreate, AddSkill
from .company_schema import CompanySignup, CompanyProfile, CompanyUpdate
from .job_schema import JobCreate, JobOut, ApplicationCreate, ApplicationOut, CandidateOut
from .problem_schema import ProblemCreate, ProblemOut, SubmissionCreate, SubmissionOut

__all__ = [
    "StudentSignup", "StudentProfile", "StudentUpdate", "ProjectCreate", "AddSkill",
    "CompanySignup", "CompanyProfile", "CompanyUpdate",
    "JobCreate", "JobOut", "ApplicationCreate", "ApplicationOut", "CandidateOut",
    "ProblemCreate", "ProblemOut", "SubmissionCreate", "SubmissionOut",
]

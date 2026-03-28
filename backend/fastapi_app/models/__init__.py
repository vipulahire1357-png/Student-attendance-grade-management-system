"""Models package — imports all ORM models so Alembic can discover them."""
from .student import Student
from .company import Company
from .job import Job, Application
from .problem import IndustryProblem, ProblemSubmission
from .skill import Skill, StudentSkill, SkillProof, Project, AIEmbedding

__all__ = [
    "Student",
    "Company",
    "Job",
    "Application",
    "IndustryProblem",
    "ProblemSubmission",
    "Skill",
    "StudentSkill",
    "SkillProof",
    "Project",
    "AIEmbedding",
]

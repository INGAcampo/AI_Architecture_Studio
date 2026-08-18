"""Validation and lookup for versioned capability-linked university courses."""
from __future__ import annotations
import json,re
from pathlib import Path
SEMVER=re.compile(r"^\d+\.\d+\.\d+$")
class UniversityCatalog:
 """Load courses and enforce identity, content, assessment and asset-link integrity."""
 def __init__(self,path:Path,known_assets:set[str]):self.data=json.loads(path.read_text(encoding="utf-8"));self.courses={x["course_id"]:x for x in self.data["courses"]};self.validate(known_assets)
 def validate(self,known_assets:set[str])->None:
  """Reject duplicate courses, invalid versions, incomplete lessons and unknown assets."""
  if len(self.courses)!=len(self.data["courses"]):raise ValueError("duplicate_course")
  for course in self.courses.values():
   if not SEMVER.fullmatch(course["version"]):raise ValueError("invalid_course_version")
   if set(course["capability_assets"])-known_assets:raise ValueError("unknown_capability_asset")
   lessons=[lesson for module in course["modules"] for lesson in module["lessons"]]
   if not lessons or any(not lesson.get("resource") for lesson in lessons):raise ValueError("incomplete_course_content")
   assessment=course["assessment"]
   if not 0<assessment["minimum_score"]<=1 or len(assessment["questions"])<3:raise ValueError("invalid_assessment")
 def get(self,course_id:str)->dict:
  """Return a course by stable identity or raise when it is unknown."""
  return self.courses[course_id]

"""Enrollment, lesson progress and deterministic assessment services."""
from __future__ import annotations
from .catalog import UniversityCatalog
class UniversityEngine:
 """Track learning progress and grade assessments without issuing credentials directly."""
 def __init__(self,catalog:UniversityCatalog):self.catalog=catalog;self.records={}
 def enroll(self,learner_id:str,course_id:str)->dict:
  """Create an idempotent learner-course record with no completed lessons."""
  course=self.catalog.get(course_id);key=(learner_id,course_id);required=[x["lesson_id"] for m in course["modules"] for x in m["lessons"]];return self.records.setdefault(key,{"learner_id":learner_id,"course_id":course_id,"required_lessons":required,"completed_lessons":[],"attempts":[],"passed":False})
 def complete_lesson(self,learner_id:str,course_id:str,lesson_id:str)->dict:
  """Mark a required lesson complete once and reject unknown lesson identities."""
  record=self.enroll(learner_id,course_id)
  if lesson_id not in record["required_lessons"]:raise ValueError("unknown_lesson")
  if lesson_id not in record["completed_lessons"]:record["completed_lessons"].append(lesson_id)
  return record
 def assess(self,learner_id:str,course_id:str,answers:dict[str,int])->dict:
  """Grade a complete answer set after all lessons and retain immutable attempt evidence."""
  record=self.enroll(learner_id,course_id)
  if set(record["completed_lessons"])!=set(record["required_lessons"]):raise PermissionError("course_content_incomplete")
  assessment=self.catalog.get(course_id)["assessment"];questions=assessment["questions"]
  if set(answers)!={q["question_id"] for q in questions}:raise ValueError("incomplete_answers")
  correct=sum(answers[q["question_id"]]==q["correct_index"] for q in questions);score=correct/len(questions);attempt={"assessment_id":assessment["assessment_id"],"score":score,"passed":score>=assessment["minimum_score"],"answers":dict(answers)};record["attempts"].append(attempt);record["passed"]=record["passed"] or attempt["passed"];return attempt
 def eligible(self,learner_id:str,course_id:str)->bool:
  """Return whether content is complete and at least one assessment attempt passed."""
  record=self.records.get((learner_id,course_id));return bool(record and record["passed"] and set(record["completed_lessons"])==set(record["required_lessons"]))

"""Dependency-safe chronological execution waves."""
def waves(rows:list[dict])->list[dict]:
 """Group non-duplicate concepts by approved chronological wave."""
 result=[]
 for number in sorted({r["wave"] for r in rows if r["declared_state"]!="DUPLICATE"}):
  items=[{"id":r["id"],"name":r["name"],"state":r["declared_state"]} for r in rows if r["wave"]==number and r["declared_state"]!="DUPLICATE"]
  result.append({"wave":number,"items":items})
 return result

def dependency_cycles(rows:list[dict])->list[str]:
 """Return nodes participating in dependency cycles."""
 graph={r["id"]:r["depends_on"] for r in rows};visiting=set();visited=set();cycles=set()
 def visit(node):
  if node in visiting:cycles.add(node);return
  if node in visited:return
  visiting.add(node)
  for dep in graph.get(node,[]):visit(dep)
  visiting.remove(node);visited.add(node)
 for node in graph:visit(node)
 return sorted(cycles)

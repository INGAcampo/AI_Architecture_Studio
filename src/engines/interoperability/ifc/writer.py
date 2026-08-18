import json
class IfcJsonWriter:
    schema="IFC4X3"
    def dumps(self, entities):
        return json.dumps({"schema":self.schema,"entities":[{"global_id":e.global_id,"kind":e.kind.value,"name":e.name,"properties":e.properties,"relationships":list(e.relationships)} for e in entities]},sort_keys=True)
    def loads(self,text):
        return json.loads(text)
class IfcStepWriter:
    schema="IFC4X3"
    def dumps(self, entities):
        lines=["ISO-10303-21;","HEADER;","FILE_SCHEMA(('IFC4X3'));","ENDSEC;","DATA;"]
        for i,e in enumerate(entities,1):
            lines.append(f"#{i}={e.kind.value.upper()}('{e.global_id}','{e.name}');")
        lines += ["ENDSEC;","END-ISO-10303-21;"]
        return "\n".join(lines)

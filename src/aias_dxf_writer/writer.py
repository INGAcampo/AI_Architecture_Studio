from pathlib import Path
class ValidDxfWriter:
 def build(self,cad):
  pairs=[]
  def add(*x): pairs.extend(map(str,x))
  add(0,'SECTION',2,'HEADER',9,'$ACADVER',1,'AC1009',0,'ENDSEC')
  add(0,'SECTION',2,'TABLES',0,'TABLE',2,'LTYPE',70,1,0,'LTYPE',2,'CONTINUOUS',70,0,3,'Solid line',72,65,73,0,40,0.0,0,'ENDTAB',0,'TABLE',2,'LAYER',70,len(cad.layers))
  for l in cad.layers: add(0,'LAYER',2,l['name'],70,0,62,l.get('color',7),6,'CONTINUOUS')
  add(0,'ENDTAB',0,'TABLE',2,'STYLE',70,1,0,'STYLE',2,'STANDARD',70,0,40,0,41,1,50,0,71,0,42,2.5,3,'txt.shx',4,'',0,'ENDTAB',0,'ENDSEC',0,'SECTION',2,'BLOCKS',0,'ENDSEC',0,'SECTION',2,'ENTITIES')
  mapping=[]
  for e in cad.entities:
   layer=e['layer']; g=e['geometry']; kind=e['kind']; mapping.append({'aias_id':e['id'],'dxf_representation':kind if kind in {'line','polyline','text'} else 'equivalent_primitives','layer':layer})
   if kind in {'line','dimension'} and isinstance(g,list) and len(g)>1: add(0,'LINE',8,layer,10,g[0][0],20,g[0][1],30,0,11,g[1][0],21,g[1][1],31,0)
   elif kind in {'polyline','rectangle'} and isinstance(g,list):
    add(0,'POLYLINE',8,layer,66,1,70,1)
    for p in g: add(0,'VERTEX',8,layer,10,p[0],20,p[1],30,0)
    add(0,'SEQEND')
   elif kind in {'text','level','bubble','block'}:
    text=e.get('attributes',{}).get('text') or e.get('attributes',{}).get('label') or e.get('attributes',{}).get('block_name') or e['id']; add(0,'TEXT',8,layer,10,0,20,0,30,0,40,2.5,1,text,7,'STANDARD')
  add(0,'ENDSEC',0,'EOF'); return '\n'.join(pairs)+'\n',mapping
 def validate(self,text):
  x=text.splitlines(); errors=[]
  if len(x)%2: errors.append('unpaired group/value')
  for token in ['SECTION','HEADER','TABLES','BLOCKS','ENTITIES','EOF']:
   if token not in x: errors.append('missing '+token)
  if x[-1:]!=['EOF']: errors.append('missing terminal EOF')
  return errors
 def write(self,cad,path):
  text,mapping=self.build(cad); errors=self.validate(text)
  if errors: raise ValueError(errors)
  Path(path).write_text(text,encoding='ascii'); return mapping

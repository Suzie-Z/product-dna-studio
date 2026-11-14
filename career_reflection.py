"""Evidence-linked recognition and possible directions, separate from map geometry."""
import copy
import career_ai as a
KEYS=('recognition','aspiration')
def section_schema():return a.obj({'text':a.text(240),'evidence_ids':a.array(a.text(24),4,1)})
def generation_schema(base):
 result=copy.deepcopy(base)
 for key in KEYS:result['properties'][key]=section_schema();result['required'].append(key)
 return result
def validate(value,map_data):
 if value is None:return None # Older session documents remain readable.
 if not isinstance(value,dict)or set(value)!=set(KEYS):raise ValueError('Invalid reflection sections')
 known={i['id']for group in ['journey','strengths']for i in map_data[group]}
 for key in KEYS:
  item=value[key];a.schema_validate(item,section_schema());a.english_field(item['text'],240,'/'+key)
  if not set(item['evidence_ids'])<=known:raise ValueError('Reflection must reference supported map evidence')
  if key=='aspiration':
   import re
   if re.search(r'\b(?:you will|you should|guaranteed|destined|qualified for|your next role is)\b',item['text'],re.I):raise ValueError('Aspiration must offer possibilities, not prescribe or promise a role')
 return copy.deepcopy(value)
GUIDANCE='''\nReturn recognition and aspiration alongside the map. Each has text (max240 characters) and evidence_ids referencing actual journey or strength IDs in this map. Recognition connects what the person did, what it demonstrates, and the transferable PM judgement they may have overlooked. Be specific about challenges, decisions or constraints, warm but restrained. Aspiration offers two possible directions or contexts to explore, based on evidenced capabilities, using conditional language. It is reflection, not job matching: no prescribed role, promotion, qualifications or guaranteed future. Never mistake a request to sound senior for evidence of leadership. Core PM capabilities must be distinct, maximum four; fewer is better than padded or overlapping categories. Evidence supports the category and what makes it distinctive. Company names, task lists and fashionable keywords are not capabilities.'''

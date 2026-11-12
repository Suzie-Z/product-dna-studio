"""Shared, bounded decorative vocabulary. Never accepts raw CSS, SVG or URLs."""
import copy,json
from pathlib import Path
MANIFEST=json.loads((Path(__file__).parent/'preview/visual-manifest.json').read_text())
def branches(previous):
 import career_ai as a
 options={'theme_id':MANIFEST['theme_ids'],'pathway_id':[p['id']for p in MANIFEST['pathways']],'character_side':['left','right'],'density':['compact','comfortable'],'contrast':['standard','high'],'softness':['standard','soft'],'decorations':['none','garden','sparkles']}
 result=[a.obj({'path':{'type':'string','enum':['/visual/'+key]},'value':{'type':'string','enum':values}})for key,values in options.items()]
 for field in ['mascot_visible','reset_icons']:result.append(a.obj({'path':{'type':'string','enum':['/visual/'+field]},'value':{'type':'boolean'}}))
 ids=[i['id']for group in ['journey','strengths']for i in previous[group]]
 result.append(a.obj({'path':{'type':'string','enum':['/visual/icons/'+i for i in ids]},'value':{'type':'string','enum':[i['id']for i in MANIFEST['icons']]}}))
 result.append(a.obj({'path':{'type':'string','enum':['/visual/platforms/'+i['id']for i in previous['journey']]},'value':{'type':'string','enum':[i['id']for i in MANIFEST['platforms']]}}))
 result.append(a.obj({'path':{'type':'string','enum':['/visual/avatar_id']},'value':{'type':'string','enum':['pm_avatar_'+str(i).zfill(2)for i in range(1,25)]}}))
 return result

def apply(current,changes,previous):
 import career_ai as a
 schema={'anyOf':branches(previous)};result=copy.deepcopy(current)if isinstance(current,dict)else{};patch={}
 for change in changes:
  a.schema_validate(change,schema);bits=change['path'].split('/')[2:];value=copy.deepcopy(change['value'])
  if len(bits)==2:
   field='icon_overrides'if bits[0]=='icons'else'platform_overrides';result.setdefault(field,{})[bits[1]]=value;patch[field]=copy.deepcopy(result[field])
  elif bits[0]=='reset_icons':
   if value:result['icon_overrides']={};patch['icon_overrides']={}
  else:result[bits[0]]=value;patch[bits[0]]=value
 return result,patch

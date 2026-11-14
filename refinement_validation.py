"""Inline edit validation, with no conversational confirmation or auto replacement."""
import re
MESSAGE="This field can't be left blank. Please enter a replacement."
def requests_blank(message):
 return bool(re.search(r'\b(?:clear|empty|blank)\b.{0,45}\b(?:title|description|theme|summary|conclusion|recognition|field)\b|\b(?:leave|make)\b.{0,45}\b(?:blank|empty)\b|\b(?:to|with)\s*["\u201c\u2018\']\s*["\u201d\u2019\']\s*[.!]?\s*$|\b(?:to|with)\s+(?:an?\s+)?(?:empty(?:\s+string)?|blank)\s*[.!]?\s*$|清空|留空|改成空',message,re.I))
def contains_blank(changes):
 for change in changes:
  if not isinstance(change,dict):continue
  value=change.get('value');path=change.get('path','')
  if isinstance(value,str)and not value.strip()and not path.endswith('/date_label'):return True
  if path in ['/strengths','/journey']and value==[]:return True
  def empty_required(node):
   if isinstance(node,dict):
    if any(key in node and isinstance(node[key],str)and not node[key].strip()for key in ['text','label','description']):return True
    return any(empty_required(v)for v in node.values())
   if isinstance(node,list):return any(empty_required(v)for v in node)
   return False
  if empty_required(value):return True
 return False

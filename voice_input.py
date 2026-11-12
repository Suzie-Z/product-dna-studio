"""Bounded in-memory multilingual transcription. No raw audio is persisted."""
import hashlib,json,os,secrets,time,urllib.request,urllib.error
from model_config import USAGE
MAX_AUDIO=8*1024*1024
MIMES={'audio/webm':'webm','audio/ogg':'ogg','audio/wav':'wav','audio/x-wav':'wav','audio/mp4':'mp4','audio/mpeg':'mp3'}
FIXTURE_TEXT='我是信任与安全产品经理。我建设安全框架，并从零到一搭建安全管线。I work on AI product evaluation and platform capabilities.'

def _request(path,body,content_type,timeout=100):
 from career_ai import AppError
 key=os.environ.get('OPENAI_API_KEY','').strip()
 if not key:raise AppError(503,'Voice transcription is not configured. You can still type.','not_configured')
 req=urllib.request.Request('https://api.openai.com/v1/'+path,data=body,headers={'Authorization':'Bearer '+key,'Content-Type':content_type})
 try:
  with urllib.request.urlopen(req,timeout=timeout)as r:return r.read()
 except urllib.error.HTTPError as e:raise AppError(503 if e.code in [401,403]else 429 if e.code==429 else 502,'Voice processing could not complete. Your recording is still available to retry.','transcription_provider_error')
 except (urllib.error.URLError,TimeoutError):raise AppError(504,'Voice processing took too long. Retry the recording or type your story.','transcription_timeout')

def validate_audio(data,mime):
 from career_ai import AppError
 mime=mime.split(';')[0].lower()
 if mime not in MIMES or not 16<=len(data)<=MAX_AUDIO:raise AppError(400,'Use a supported recording under 8 MB.','invalid_audio')
 signatures={'webm':data.startswith(b'\x1aE\xdf\xa3'),'ogg':data.startswith(b'OggS'),'wav':data.startswith(b'RIFF')and data[8:12]==b'WAVE','mp4':data[4:8]==b'ftyp','mp3':data.startswith(b'ID3')or(data[0]==255 and data[1]&224==224)}
 if not signatures[MIMES[mime]]:raise AppError(400,'The recording format could not be read. Please record again.','invalid_audio')
 return mime

def transcribe(data,mime):
 from career_ai import reserve_attempt,AppError
 mime=validate_audio(data,mime);model=os.environ.get('OPENAI_TRANSCRIPTION_MODEL','gpt-transcribe').strip();boundary='pmvoice'+secrets.token_hex(16);parts=[]
 def field(key,value):parts.append(('--'+boundary+'\r\nContent-Disposition: form-data; name="'+key+'"\r\n\r\n'+value+'\r\n').encode())
 field('model',model);field('prompt','Faithfully transcribe the original languages. Speech may mix Mandarin and English PM terms: AI, Trust & Safety, safety frameworks, zero-to-one pipelines, model evaluation. Do not translate or add words not spoken.')
 parts.append(('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="recording.'+MIMES[mime]+'"\r\nContent-Type: '+mime+'\r\n\r\n').encode()+data+b'\r\n');parts.append(('--'+boundary+'--\r\n').encode());reserve_attempt();started=time.monotonic();response=json.loads(_request('audio/transcriptions',b''.join(parts),'multipart/form-data; boundary='+boundary));text=response.get('text','').strip()
 if not text:raise AppError(422,'No speech was detected. You can record again or type.','no_speech')
 if len(text)>18000:raise AppError(413,'The transcript is too long. Record a shorter segment.','transcript_too_long')
 if USAGE.get()is not None:USAGE.get().append({'stage':'transcription','model':model,'provider_model':response.get('model',model),'seconds':round(time.monotonic()-started,2),'usage':response.get('usage',{})})
 return {'text':text,'transcription_model':model,'languages':response.get('languages',[])}

def synthetic_fixture():
 """Authenticated test-only fixed speech sample, never a visitor-facing TTS feature."""
 from career_ai import reserve_attempt
 model='gpt-4o-mini-tts';reserve_attempt();return _request('audio/speech',json.dumps({'model':model,'voice':'alloy','input':FIXTURE_TEXT,'response_format':'mp3'}).encode(),'application/json')

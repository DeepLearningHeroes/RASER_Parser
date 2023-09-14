import pickle
import pathlib
pathlib.PosixPath = pathlib.WindowsPath

import sys
import fitz

def nlpParser(fname):
  doc=fitz.open(fname)
  text=""
  for page in doc:
    text=text+str(page.get_text())

  ' '.join(text.split())

  pkl_filename = 'model.pkl'
  with open(pkl_filename,'rb') as file:
    model=pickle.load(file)

  doc=model(text)
  entity_dict={}
  for ent in doc.ents:
    # print(ent.text,"---->",ent.label_)
    if ent.label_ not in entity_dict:
      entity_dict[ent.label_]=[ent.text]
    elif ent.text not in entity_dict[ent.label_]:
      entity_dict[ent.label_].append(ent.text)

  return entity_dict

from pathlib import Path
from src.storage.project_io import ProjectIO
from src.models.project.project_document import ProjectDocument
def test_create_save_and_load_project(tmp_path:Path):
    io=ProjectIO(); doc=io.new_project('Casa Demo'); doc.add_object({'id':'line-001','type':'LINE','start':[0,0,0],'end':[5,0,0],'layer':'0'})
    path=io.save(doc,tmp_path/'Casa_Demo.aias'); loaded=io.open(path)
    assert path.exists() and loaded.metadata.name=='Casa Demo' and loaded.objects[0]['type']=='LINE' and not loaded.dirty
def test_document_api(tmp_path:Path):
    doc=ProjectDocument.create('Edificio'); path=doc.save(tmp_path/'Edificio.aias'); assert ProjectDocument.load(path).metadata.name=='Edificio'

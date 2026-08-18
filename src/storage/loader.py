from pathlib import Path
import json,zipfile
from models.project.metadata import ProjectMetadata
from models.project.settings import ProjectSettings
from models.project.project_document import ProjectDocument
from .checksum import verify_checksum
from .file_version import AIAS_FILE_VERSION,FileVersion
from .serializer import ProjectSerializer
class InvalidAIASFileError(RuntimeError): pass
class IncompatibleAIASVersionError(RuntimeError): pass
class ProjectLoader:
    def load(self,source):
        source=Path(source)
        if not source.exists(): raise FileNotFoundError(source)
        if source.suffix.lower()!='.aias': raise InvalidAIASFileError('El archivo debe tener extensión .aias')
        try:
            with zipfile.ZipFile(source,'r') as z:
                required={ProjectSerializer.MANIFEST_FILE,ProjectSerializer.METADATA_FILE,ProjectSerializer.DRAWING_FILE,ProjectSerializer.SETTINGS_FILE}
                missing=required-set(z.namelist())
                if missing: raise InvalidAIASFileError(f'Faltan archivos internos: {sorted(missing)}')
                read=lambda n: json.loads(z.read(n).decode('utf-8'))
                manifest=read(ProjectSerializer.MANIFEST_FILE); metadata=read(ProjectSerializer.METADATA_FILE); drawing=read(ProjectSerializer.DRAWING_FILE); settings=read(ProjectSerializer.SETTINGS_FILE)
        except zipfile.BadZipFile as e: raise InvalidAIASFileError('Archivo .aias dañado') from e
        if manifest.get('format')!='AIAS': raise InvalidAIASFileError('Formato no reconocido')
        fv=FileVersion.parse(manifest.get('file_version','0.0.0')); sv=FileVersion.parse(AIAS_FILE_VERSION)
        if not fv.is_compatible_with(sv): raise IncompatibleAIASVersionError(f'Versión {fv} no compatible con {sv}')
        payloads={ProjectSerializer.METADATA_FILE:metadata,ProjectSerializer.DRAWING_FILE:drawing,ProjectSerializer.SETTINGS_FILE:settings}
        for n,p in payloads.items():
            if not verify_checksum(p,manifest.get('checksums',{}).get(n,'')): raise InvalidAIASFileError(f'Integridad fallida en {n}')
        doc=ProjectDocument(metadata=ProjectMetadata.from_dict(metadata),settings=ProjectSettings.from_dict(settings),objects=list(drawing.get('objects',[])),layers=list(drawing.get('layers',[])),camera=dict(drawing.get('camera',{})),custom_data=dict(drawing.get('custom_data',{})),file_path=source)
        doc.mark_clean(); return doc

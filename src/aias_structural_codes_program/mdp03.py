"""MDP-03 governed GIS, road corridor, earthwork and urban asset model."""
from __future__ import annotations

from dataclasses import asdict,dataclass
import hashlib,json,math
from .mdp02 import EngineeringStudyContext


@dataclass(frozen=True,slots=True)
class SpatialReference:
    authority:str;code:int;vertical_datum:str;linear_units:str="m"
    def validate(self)->list[str]:
        issues=[]
        if self.authority not in {"EPSG","PROJECT_AUTHORITY"} or self.code<=0:issues.append("invalid_horizontal_crs")
        if not self.vertical_datum:issues.append("vertical_datum_required")
        if self.linear_units!="m":issues.append("unsupported_spatial_units")
        return issues


@dataclass(frozen=True,slots=True)
class SurveyPoint:
    point_id:str;x:float;y:float;z:float;source_id:str


@dataclass(frozen=True,slots=True)
class AlignmentStation:
    station_m:float;x:float;y:float;design_elevation_m:float


@dataclass(frozen=True,slots=True)
class EarthworkSection:
    station_m:float;cut_area_m2:float;fill_area_m2:float


@dataclass(frozen=True,slots=True)
class UrbanAsset:
    asset_id:str;asset_type:str;x:float;y:float;z:float;source_id:str


@dataclass(frozen=True,slots=True)
class CivilSpatialModel:
    model_id:str;revision:str;context:EngineeringStudyContext;crs:SpatialReference;survey_points:tuple[SurveyPoint,...];alignment:tuple[AlignmentStation,...];earthwork_sections:tuple[EarthworkSection,...];urban_assets:tuple[UrbanAsset,...]
    def validate(self)->list[str]:
        issues=self.context.validate()+self.crs.validate()
        if not self.model_id or not self.revision:issues.append("civil_model_identity_incomplete")
        known={x.source_id for x in self.context.sources}
        def unique(rows,attribute,label):
            values=[getattr(x,attribute) for x in rows]
            if len(values)!=len(set(values)):issues.append(f"duplicate_{label}")
        unique(self.survey_points,"point_id","survey_point");unique(self.urban_assets,"asset_id","urban_asset")
        for row in (*self.survey_points,*self.urban_assets):
            if not all(math.isfinite(v) for v in (row.x,row.y,row.z)):issues.append(f"{getattr(row,'point_id',getattr(row,'asset_id',''))}:non_finite_coordinate")
            if row.source_id not in known:issues.append(f"{getattr(row,'point_id',getattr(row,'asset_id',''))}:unknown_source_id")
        if len(self.alignment)<2:issues.append("alignment_requires_two_stations")
        stations=[x.station_m for x in self.alignment]
        if any(not math.isfinite(x) for x in stations) or any(b<=a for a,b in zip(stations,stations[1:])):issues.append("alignment_stations_not_strictly_increasing")
        section_stations=[x.station_m for x in self.earthwork_sections]
        if len(section_stations)<2:issues.append("earthwork_requires_two_sections")
        if any(b<=a for a,b in zip(section_stations,section_stations[1:])):issues.append("earthwork_stations_not_strictly_increasing")
        for row in self.earthwork_sections:
            if min(row.cut_area_m2,row.fill_area_m2)<0:issues.append(f"earthwork:{row.station_m}:negative_area")
        allowed={"ROAD","WATER","SANITARY","STORMWATER","POWER","TELECOM","PARCEL","STRUCTURE","PUBLIC_SPACE"}
        for row in self.urban_assets:
            if row.asset_type not in allowed:issues.append(f"{row.asset_id}:unsupported_asset_type")
        return issues
    def sha256(self)->str:
        payload=json.dumps(asdict(self),sort_keys=True,separators=(",",":"),ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True,slots=True)
class CivilSpatialResult:
    model_id:str;crs:str;alignment_length_m:float;maximum_absolute_grade:float;cut_volume_m3:float;fill_volume_m3:float;earthwork_balance_m3:float;urban_asset_count:int;model_sha256:str;issues:tuple[str,...];normative_compliance_claimed:bool;construction_approved:bool=False


class CivilInfrastructureEngine:
    """Summarize a traceable civil model using explicit, reproducible quantities."""
    def evaluate(self,model:CivilSpatialModel)->CivilSpatialResult:
        issues=model.validate();length=0.0;grades=[]
        if len(model.alignment)>=2:
            length=model.alignment[-1].station_m-model.alignment[0].station_m
            for first,last in zip(model.alignment,model.alignment[1:]):
                distance=last.station_m-first.station_m
                if distance>0:
                    grades.append((last.design_elevation_m-first.design_elevation_m)/distance)
        cut=fill=0.0
        for first,last in zip(model.earthwork_sections,model.earthwork_sections[1:]):
            distance=last.station_m-first.station_m
            if distance>0:
                cut+=(first.cut_area_m2+last.cut_area_m2)*.5*distance
                fill+=(first.fill_area_m2+last.fill_area_m2)*.5*distance
        normative=not issues and model.context.normative_claim_allowed()
        return CivilSpatialResult(model.model_id,f"{model.crs.authority}:{model.crs.code}",length,max((abs(x) for x in grades),default=0.0),cut,fill,cut-fill,len(model.urban_assets),model.sha256(),tuple(issues),normative,False)

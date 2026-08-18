"""Semantic visual tokens shared by desktop, web, installers and documents."""
from __future__ import annotations

def design_tokens()->dict:
    return {
        "system":"AIAS-DESIGN-SYSTEM",
        "version":"0.1.0",
        "status":"FOUNDATION_CANDIDATE_FOR_RENDERED_REVIEW",
        "typography":{"ui":["Inter","Segoe UI","Noto Sans","sans-serif"],"mono":["JetBrains Mono","Cascadia Mono","monospace"],"scale_px":{"xs":12,"sm":13,"md":15,"lg":18,"xl":24,"display":32},"minimum_body_px":13},
        "spacing":{"unit_px":4,"scale_px":[0,4,8,12,16,24,32,48,64]},
        "radius_px":{"sm":4,"md":8,"lg":12,"pill":999},
        "motion_ms":{"instant":0,"fast":120,"standard":180,"deliberate":260,"reduced":0},
        "iconography":{"grid_px":24,"stroke_px":1.75,"sizes_px":[16,20,24,32],"style":"geometric_line_with_solid_state_variants","random_external_icons_prohibited":True},
        "dark":{"background":"#0B111A","surface":"#111B29","surface_elevated":"#172438","border":"#2B3C52","text":"#F5F7FA","text_muted":"#AFC0D4","accent":"#36A3FF","on_accent":"#06121F","focus":"#72C1FF","success":"#3CCB7F","warning":"#FFB547","danger":"#FF5C67","canvas":"#071018","selection":"#164C73"},
        "light":{"background":"#F3F6FA","surface":"#FFFFFF","surface_elevated":"#EAF0F6","border":"#A9B8C8","text":"#132033","text_muted":"#53677E","accent":"#0869B3","on_accent":"#FFFFFF","focus":"#005FA8","success":"#147A46","warning":"#8A5200","danger":"#B4232C","canvas":"#FFFFFF","selection":"#CDEAFF"},
        "breakpoints_px":{"compact":720,"standard":1024,"wide":1440,"ultrawide":1920},
        "accessibility":{"minimum_contrast_normal":4.5,"minimum_contrast_large":3.0,"keyboard_visible_focus":True,"minimum_target_px":32,"preferred_target_px":40,"color_only_state_prohibited":True,"reduced_motion_required":True},
    }

def validate_tokens(tokens:dict)->list[str]:
    issues=[]
    required={"background","surface","surface_elevated","border","text","text_muted","accent","on_accent","focus","success","warning","danger","canvas","selection"}
    for theme in ("dark","light"):
        missing=required-set(tokens.get(theme,{}))
        if missing:issues.append(f"{theme}:missing:{sorted(missing)}")
        for key,value in tokens.get(theme,{}).items():
            if not isinstance(value,str) or len(value)!=7 or not value.startswith("#"):issues.append(f"{theme}:{key}:invalid_color")
    if tokens.get("accessibility",{}).get("minimum_contrast_normal",0)<4.5:issues.append("contrast_policy_below_wcag_aa")
    if tokens.get("typography",{}).get("minimum_body_px",0)<13:issues.append("minimum_body_text_too_small")
    if tokens.get("iconography",{}).get("random_external_icons_prohibited") is not True:issues.append("icon_governance_missing")
    return issues

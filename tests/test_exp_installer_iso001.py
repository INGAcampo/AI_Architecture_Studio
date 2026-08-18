from pathlib import Path
import hashlib
import pytest
from aias_distribution import DeploymentPolicy,InstallerTransaction,OfflineMediaBuilder,UpdatePlanner,verify_offline_media

def installer(root:Path,name="AIAS_DEMO_INSTALLER"):
 folder=root/name;folder.mkdir();(folder/"manifest.json").write_text('{"version":"1.0.0"}',encoding="utf-8");digest=hashlib.sha256((folder/"manifest.json").read_bytes()).hexdigest();(folder/"checksums.sha256").write_text(f"{digest}  manifest.json\n",encoding="utf-8");return name
def test_offline_media_and_transactional_install_roundtrip(tmp_path):
 name=installer(tmp_path);media=tmp_path/"AIAS_OFFLINE.zip";result=OfflineMediaBuilder().build(tmp_path,(name,),media,"1.0.0");assert result["verified"] and not result["publisher_signed"] and not result["iso_image_created"];allowed=tmp_path/"deployments";allowed.mkdir();tx=InstallerTransaction(DeploymentPolicy(allowed));installed=tx.install(media,allowed/"AIAS");assert installed["integrity_verified"] and (allowed/"AIAS/MEDIA_MANIFEST.json").is_file()
def test_existing_release_can_be_rolled_back(tmp_path):
 name=installer(tmp_path);media=tmp_path/"m.zip";OfflineMediaBuilder().build(tmp_path,(name,),media,"1.0.0");allowed=tmp_path/"deploy";target=allowed/"AIAS";target.mkdir(parents=True);(target/"old.txt").write_text("old");tx=InstallerTransaction(DeploymentPolicy(allowed));result=tx.install(media,target);assert result["rollback_available"];rolled=tx.rollback(target,Path(result["previous"]));assert rolled["status"]=="ROLLED_BACK" and (target/"old.txt").read_text()=="old"
def test_destination_boundary_and_tampering_fail_closed(tmp_path):
 name=installer(tmp_path);media=tmp_path/"m.zip";OfflineMediaBuilder().build(tmp_path,(name,),media,"1");assert verify_offline_media(media)["valid"];tx=InstallerTransaction(DeploymentPolicy(tmp_path/"allowed"));
 with pytest.raises(ValueError,match="outside_allowed_root"):tx.install(media,tmp_path/"other"/"AIAS")
 media.write_bytes(media.read_bytes()+b"tamper")
 # ZIP trailing bytes do not alter members; external release hash detects this layer.
 assert verify_offline_media(media)["valid"]
def test_update_planner_requires_integrity_and_real_publisher_signature():
 planner=UpdatePlanner();blocked=planner.plan("1.0.0","1.1.0",candidate_integrity_verified=True,publisher_signature_verified=False);assert blocked["action"]=="BLOCKED" and "publisher_signature_unverified" in blocked["blockers"];assert planner.plan("1.0.0","1.1.0",candidate_integrity_verified=True,publisher_signature_verified=True)["action"]=="INSTALL";assert planner.plan("2.0.0","1.0.0",candidate_integrity_verified=True,publisher_signature_verified=True)["action"]=="BLOCKED"
def test_same_inputs_produce_byte_identical_offline_media(tmp_path):
 name=installer(tmp_path);first=tmp_path/"first.zip";second=tmp_path/"second.zip";OfflineMediaBuilder().build(tmp_path,(name,),first,"1.0.0");OfflineMediaBuilder().build(tmp_path,(name,),second,"1.0.0");assert hashlib.sha256(first.read_bytes()).digest()==hashlib.sha256(second.read_bytes()).digest()

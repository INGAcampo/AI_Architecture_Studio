from pathlib import Path
from aias_central_nervous_system import NervousSystemBus,Event
from aias_central_nervous_system.projection import CompanyStateProjection
def test_durable_idempotent_publication(tmp_path):
 bus=NervousSystemBus(tmp_path/"journal.json");event=Event.create("delivery.completed","PMO",{"id":"D-1"});first=bus.publish(event);second=bus.publish(event);assert first["sequence"]==second["sequence"] and len(bus.journal.data["events"])==1
def test_ordered_delivery_cursor_and_projection(tmp_path):
 bus=NervousSystemBus(tmp_path/"journal.json");projection=CompanyStateProjection();bus.subscribe("AIPD",{"delivery.completed"},projection.apply)
 bus.publish(Event.create("delivery.completed","PMO",{"id":"D-1"}));bus.publish(Event.create("delivery.completed","PMO",{"id":"D-2"}));result=bus.dispatch("AIPD");assert result["delivered"]==2 and [x["id"] for x in projection.state["deliveries"]]==["D-1","D-2"] and bus.dispatch("AIPD")["delivered"]==0
def test_failed_delivery_is_dead_lettered_without_cursor_advance(tmp_path):
 bus=NervousSystemBus(tmp_path/"journal.json");bus.subscribe("FAIL",{"risk.raised"},lambda event:(_ for _ in ()).throw(RuntimeError("boom")));bus.publish(Event.create("risk.raised","SECURITY",{"risk":"R"}));result=bus.dispatch("FAIL");assert result["failed"]==1 and result["cursor"]==0 and len(bus.journal.data["dead_letters"])==1
def test_payload_and_cursor_validation(tmp_path):
 import pytest
 bus=NervousSystemBus(tmp_path/"journal.json")
 with pytest.raises(ValueError):bus.publish(Event("BAD","invalid","","","","1.0.0",{}))
 bus.publish(Event.create("context.updated","ACE",{}))
 with pytest.raises(ValueError):bus.journal.acknowledge("X",2)

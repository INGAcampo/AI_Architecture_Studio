"""
AI Architecture Studio
CAD Renderer

Dynamic Input v2 - Package 3 / UI 2.4
"""

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QBrush, QFont, QPainterPath, QPen, QPolygonF, QRegion

from engines.cad.coordinates import CoordinateSystem
from engines.architectural.wall_network import WallNetwork


class Renderer:

    def __init__(self):
        self.default_pen = QPen(QColor(220, 220, 220), 2)
        self.preview_pen = QPen(QColor(80, 220, 120), 1)
        self.highlight_pen = QPen(QColor(255, 210, 0), 3)
        self.selection_pen = QPen(QColor(0, 170, 255), 3)
        self.snap_pen = QPen(QColor(0, 255, 255), 2)
        self.window_pen = QPen(QColor(60, 150, 255), 1)
        self.crossing_pen = QPen(QColor(70, 220, 120), 1)
        self.dynamic_border_pen = QPen(QColor(115, 185, 255), 1)
        self.dynamic_active_pen = QPen(QColor(255, 210, 70), 2)

        self.dynamic_background = QBrush(QColor(30, 34, 40, 235))
        self.dynamic_active_background = QBrush(QColor(65, 56, 24, 245))
        self.dynamic_inactive_background = QBrush(QColor(43, 48, 56, 240))

        self.coordinates = CoordinateSystem()

    def _set_entity_pen(
        self,
        painter,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        if selected:
            painter.setPen(self.selection_pen)
        elif highlighted:
            painter.setPen(self.highlight_pen)
        elif preview:
            painter.setPen(self.preview_pen)
        else:
            painter.setPen(self.default_pen)

    def draw_line(
        self,
        painter,
        camera,
        line,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            preview=preview,
            highlighted=highlighted,
            selected=selected,
        )

        x1, y1 = self.coordinates.world_to_screen(
            line.start.x,
            line.start.y,
            camera,
        )
        x2, y2 = self.coordinates.world_to_screen(
            line.end.x,
            line.end.y,
            camera,
        )

        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_polyline(
        self,
        painter,
        camera,
        polyline,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            highlighted=highlighted,
            selected=selected,
        )

        getter = getattr(polyline, "get_segments", None)

        if callable(getter):
            segments = getter()
        else:
            segments = []

        if segments:
            for segment in segments:
                kind = segment.__class__.__name__

                if kind == "Line":
                    self.draw_line(
                        painter,
                        camera,
                        segment,
                        highlighted=highlighted,
                        selected=selected,
                    )
                elif kind == "CadArc":
                    self.draw_arc(
                        painter,
                        camera,
                        segment,
                        highlighted=highlighted,
                        selected=selected,
                    )

            return

        points = polyline.points

        if len(points) < 2:
            return

        for index in range(len(points) - 1):
            self.draw_line(
                painter,
                camera,
                type(
                    "_PreviewLine",
                    (),
                    {
                        "start": points[index],
                        "end": points[index + 1],
                    },
                )(),
                highlighted=highlighted,
                selected=selected,
            )

        if polyline.closed and len(points) > 2:
            self.draw_line(
                painter,
                camera,
                type(
                    "_PreviewLine",
                    (),
                    {
                        "start": points[-1],
                        "end": points[0],
                    },
                )(),
                highlighted=highlighted,
                selected=selected,
            )

    def draw_circle(
        self,
        painter,
        camera,
        circle,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            preview=preview,
            highlighted=highlighted,
            selected=selected,
        )

        center_x, center_y = self.coordinates.world_to_screen(
            circle.center.x,
            circle.center.y,
            camera,
        )

        radius_pixels = (
            circle.radius
            * self.coordinates.scale
            * camera.zoom
        )

        painter.drawEllipse(
            int(center_x - radius_pixels),
            int(center_y - radius_pixels),
            int(radius_pixels * 2),
            int(radius_pixels * 2),
        )


    def draw_arc(
        self,
        painter,
        camera,
        arc,
        preview=False,
        highlighted=False,
        selected=False,
    ):
        self._set_entity_pen(
            painter,
            preview=preview,
            highlighted=highlighted,
            selected=selected,
        )

        segments = max(
            12,
            int(abs(arc.sweep_angle) * 24),
        )

        polygon = QPolygonF()

        for index in range(segments + 1):
            point = arc.point_at(index / segments)
            screen_x, screen_y = (
                self.coordinates.world_to_screen(
                    point.x,
                    point.y,
                    camera,
                )
            )
            polygon.append(
                QPointF(screen_x, screen_y)
            )

        painter.drawPolyline(polygon)


    def _wall_polygon_to_path(self,camera,points):
        polygon=QPolygonF()
        for point in points:
            x,y=self.coordinates.world_to_screen(point.x,point.y,camera)
            polygon.append(QPointF(x,y))
        path=QPainterPath(); path.addPolygon(polygon); path.closeSubpath(); return path

    def wall_path(self,camera,wall,use_segment_union=False):
        from engines.architectural.wall_engine import WallEngine
        from engines.architectural.opening_engine import OpeningEngine

        polygons=(
            WallEngine.build_segment_polygons(wall)
            if use_segment_union
            else WallEngine.build_wall_geometry(wall)
        )
        result=QPainterPath()
        for points in polygons:
            candidate=self._wall_polygon_to_path(camera,points)
            result=candidate if result.isEmpty() else result.united(candidate)

        # OPENING CORE 5.0.5.1: sustrae huecos paramétricos.
        for opening in list(getattr(wall,"openings",[]) or []):
            if not getattr(opening,"visible",True):
                continue
            cutter_points=OpeningEngine.cutter_polygon(opening)
            if not cutter_points:
                continue
            cutter=self._wall_polygon_to_path(camera,cutter_points)
            result=result.subtracted(cutter)

        return result

    def draw_door(self,painter,camera,door):
        from engines.architectural.door_engine import DoorEngine

        if door is None or not getattr(door,"visible",True):
            return

        painter.save()
        painter.setBrush(QBrush(Qt.NoBrush))

        # Marco.
        painter.setPen(QPen(QColor(235,235,235,235),2))
        for first,second in DoorEngine.frame_lines(door):
            x1,y1=self.coordinates.world_to_screen(first.x,first.y,camera)
            x2,y2=self.coordinates.world_to_screen(second.x,second.y,camera)
            painter.drawLine(int(x1),int(y1),int(x2),int(y2))

        # Hoja abierta.
        leaf=DoorEngine.leaf_line(door)
        if leaf is not None:
            first,second=leaf
            x1,y1=self.coordinates.world_to_screen(first.x,first.y,camera)
            x2,y2=self.coordinates.world_to_screen(second.x,second.y,camera)
            painter.setPen(QPen(QColor(255,205,70,245),2))
            painter.drawLine(int(x1),int(y1),int(x2),int(y2))

        # Arco de giro.
        arc_points=DoorEngine.swing_arc_points(door)
        if len(arc_points)>=2:
            polygon=QPolygonF()
            for point in arc_points:
                x,y=self.coordinates.world_to_screen(point.x,point.y,camera)
                polygon.append(QPointF(x,y))
            painter.setPen(QPen(QColor(255,205,70,210),1,Qt.DashLine))
            painter.drawPolyline(polygon)

        painter.restore()

    def draw_window(self,painter,camera,window):
        from engines.architectural.window_engine import WindowEngine
        geometry=WindowEngine.plan_geometry(window)
        if geometry is None:return
        painter.save();painter.setBrush(QBrush(Qt.NoBrush));painter.setPen(QPen(QColor(100,210,255,245),2))
        for first,second in geometry["frame"]:
            x1,y1=self.coordinates.world_to_screen(first.x,first.y,camera);x2,y2=self.coordinates.world_to_screen(second.x,second.y,camera);painter.drawLine(int(x1),int(y1),int(x2),int(y2))
        first,second=geometry["mullion"];x1,y1=self.coordinates.world_to_screen(first.x,first.y,camera);x2,y2=self.coordinates.world_to_screen(second.x,second.y,camera);painter.drawLine(int(x1),int(y1),int(x2),int(y2));painter.restore()

    def draw_wall_hosted_elements(self,painter,camera,walls):
        for wall in walls:
            for opening in list(getattr(wall,"openings",[]) or []):
                door=getattr(opening,"door",None)
                if door is not None:self.draw_door(painter,camera,door)
                window=getattr(opening,"window",None)
                if window is not None:self.draw_window(painter,camera,window)



    def draw_slab(self,painter,camera,slab,highlighted=False,selected=False):
        if slab is None or not getattr(slab,"visible",True):
            return
        if not getattr(slab,"valid",False):
            return

        boundary=list(getattr(slab,"boundary",[]) or [])
        if len(boundary)<3:
            return

        polygon=QPolygonF()
        screen_points=[]
        for point in boundary:
            x,y=self.coordinates.world_to_screen(point.x,point.y,camera)
            polygon.append(QPointF(x,y))
            screen_points.append((x,y))

        painter.save()
        if selected:
            pen=self.selection_pen
        elif highlighted:
            pen=self.highlight_pen
        else:
            pen=QPen(QColor(210,170,90,210),2,Qt.DashDotLine)

        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(210,170,90,22)))
        painter.drawPolygon(polygon)

        # Trama diagonal ligera para distinguir la losa del ROOM.
        if screen_points:
            min_x=min(point[0] for point in screen_points)
            max_x=max(point[0] for point in screen_points)
            min_y=min(point[1] for point in screen_points)
            max_y=max(point[1] for point in screen_points)
            painter.setClipRegion(QRegion(polygon.toPolygon()))
            painter.setPen(QPen(QColor(210,170,90,75),1))
            spacing=18
            start=int(min_x-(max_y-min_y))-spacing
            end=int(max_x+(max_y-min_y))+spacing
            for offset in range(start,end,spacing):
                painter.drawLine(
                    int(offset),int(max_y),
                    int(offset+(max_y-min_y)),int(min_y),
                )
        painter.restore()

    def draw_room(self,painter,camera,room,highlighted=False,selected=False):
        if room is None or not getattr(room,"visible",True):
            return
        if not getattr(room,"valid",False):
            return

        boundary=list(getattr(room,"boundary",[]) or [])
        if len(boundary)<3:
            return

        polygon=QPolygonF()
        for point in boundary:
            x,y=self.coordinates.world_to_screen(point.x,point.y,camera)
            polygon.append(QPointF(x,y))

        painter.save()
        if selected:
            pen=self.selection_pen
            fill=QColor(0,170,255,55)
        elif highlighted:
            pen=self.highlight_pen
            fill=QColor(255,210,0,45)
        else:
            pen=QPen(QColor(90,190,255,170),1,Qt.DashLine)
            category=getattr(room,"category","generic")
            category_colors={
                "generic":QColor(70,150,220,30),
                "living":QColor(230,180,70,38),
                "bedroom":QColor(120,150,235,38),
                "kitchen":QColor(235,135,70,38),
                "bathroom":QColor(80,190,210,38),
                "service":QColor(155,155,155,38),
                "circulation":QColor(190,170,110,34),
                "exterior":QColor(90,190,110,34),
            }
            fill=category_colors.get(
                category,
                category_colors["generic"],
            )

        painter.setPen(pen)
        painter.setBrush(QBrush(fill))
        painter.drawPolygon(polygon)

        label=getattr(room,"label_position",None)
        if label is not None:
            x,y=self.coordinates.world_to_screen(label.x,label.y,camera)
            painter.setPen(QPen(QColor(225,235,245,240),1))
            painter.setBrush(QBrush(QColor(30,36,44,210)))
            font=QFont(painter.font())
            font.setPointSize(9)
            painter.setFont(font)
            number=str(getattr(room,"number","") or "").strip()
            room_name=str(getattr(room,"name","Ambiente"))
            line1=f"{number} - {room_name}" if number else room_name
            line2=f"{getattr(room,'area',0.0):.2f} m²"
            width=max(96,len(line1)*7,len(line2)*7)
            rect=QRectF(x-width/2,y-23,width,42)
            painter.drawRoundedRect(rect,4,4)
            painter.drawText(
                QRectF(rect.x()+4,rect.y()+3,rect.width()-8,17),
                Qt.AlignCenter,
                line1,
            )
            painter.drawText(
                QRectF(rect.x()+4,rect.y()+20,rect.width()-8,17),
                Qt.AlignCenter,
                line2,
            )
        painter.restore()

    def draw_wall_network(self,painter,camera,walls):
        path=QPainterPath()
        for wall in walls:
            candidate=self.wall_path(camera,wall,True)
            if candidate.isEmpty(): continue
            path=candidate if path.isEmpty() else path.united(candidate)
        if not path.isEmpty():
            painter.save()
            painter.setPen(self.default_pen)
            painter.setBrush(QBrush(QColor(145,150,158,105)))
            painter.drawPath(path)
            painter.restore()

        # DOOR 5.0.5.2.1: los elementos alojados se dibujan
        # después de la unión booleana de todos los muros.
        self.draw_wall_hosted_elements(painter,camera,walls)

    def draw_wall(self,painter,camera,wall,preview=False,highlighted=False,selected=False):
        path=self.wall_path(camera,wall,preview)
        if path.isEmpty(): return
        painter.save()
        if selected: pen,fill=self.selection_pen,QColor(0,170,255,85)
        elif highlighted: pen,fill=self.highlight_pen,QColor(255,210,0,80)
        elif preview: pen,fill=self.preview_pen,QColor(80,220,120,70)
        else: pen,fill=self.default_pen,QColor(145,150,158,105)
        painter.setPen(pen); painter.setBrush(QBrush(fill)); painter.drawPath(path)
        painter.setPen(QPen(QColor(185,190,198,150),1,Qt.DashLine)); painter.setBrush(QBrush(Qt.NoBrush))
        for i in range(len(wall.path)-1):
            a,b=wall.path[i],wall.path[i+1]
            x1,y1=self.coordinates.world_to_screen(a.x,a.y,camera); x2,y2=self.coordinates.world_to_screen(b.x,b.y,camera)
            painter.drawLine(int(x1),int(y1),int(x2),int(y2))

        # Jambas del hueco en planta.
        from engines.architectural.opening_engine import OpeningEngine
        painter.setPen(QPen(QColor(230,235,240,220),1))
        for opening in list(getattr(wall,"openings",[]) or []):
            for first,second in OpeningEngine.jamb_lines(opening):
                x1,y1=self.coordinates.world_to_screen(first.x,first.y,camera)
                x2,y2=self.coordinates.world_to_screen(second.x,second.y,camera)
                painter.drawLine(int(x1),int(y1),int(x2),int(y2))
        painter.restore()

    def draw_snap_marker(
        self,
        painter,
        camera,
        point,
        snap_type,
        show_label=True,
    ):
        if point is None or snap_type is None:
            return

        screen_x, screen_y = self.coordinates.world_to_screen(
            point.x,
            point.y,
            camera,
        )

        x = int(screen_x)
        y = int(screen_y)
        size = 7

        painter.setPen(self.snap_pen)

        if snap_type == "Endpoint":
            painter.drawRect(
                x - size,
                y - size,
                size * 2,
                size * 2,
            )
        elif snap_type == "Midpoint":
            painter.drawLine(x, y - size, x - size, y + size)
            painter.drawLine(x - size, y + size, x + size, y + size)
            painter.drawLine(x + size, y + size, x, y - size)
        elif snap_type == "Center":
            painter.drawEllipse(
                x - size,
                y - size,
                size * 2,
                size * 2,
            )
            painter.drawLine(x - size, y, x + size, y)
            painter.drawLine(x, y - size, x, y + size)
        elif snap_type == "Intersection":
            painter.drawLine(x - size, y - size, x + size, y + size)
            painter.drawLine(x - size, y + size, x + size, y - size)
        elif snap_type == "Nearest":
            painter.drawEllipse(x - 4, y - 4, 8, 8)
        elif snap_type == "Grid":
            painter.drawLine(x - size, y, x + size, y)
            painter.drawLine(x, y - size, x, y + size)

        if show_label:
            painter.drawText(x + 12, y - 10, snap_type)

    def draw_selection_window(
        self,
        painter,
        camera,
        first_point,
        second_point,
        crossing=False,
    ):
        if first_point is None or second_point is None:
            return

        x1, y1 = self.coordinates.world_to_screen(
            first_point.x,
            first_point.y,
            camera,
        )
        x2, y2 = self.coordinates.world_to_screen(
            second_point.x,
            second_point.y,
            camera,
        )

        left = int(min(x1, x2))
        top = int(min(y1, y2))
        width = max(1, int(abs(x2 - x1)))
        height = max(1, int(abs(y2 - y1)))

        if crossing:
            painter.setPen(self.crossing_pen)
            painter.setBrush(QBrush(QColor(50, 180, 90, 45)))
        else:
            painter.setPen(self.window_pen)
            painter.setBrush(QBrush(QColor(50, 120, 230, 45)))

        painter.drawRect(left, top, width, height)
        painter.setBrush(QBrush(Qt.NoBrush))

    def draw_dynamic_input(
        self,
        painter,
        manager,
   ):
        if manager is None:
            return

        if not hasattr(manager, "formatted_distance"):
            return

        if not getattr(manager, "enabled", False):
            return

        if not getattr(manager, "visible", False):
            return

        x = int(manager.screen_x)
        y = int(manager.screen_y)

        panel_width = 174
        row_height = 27
        padding = 7
        prompt_height = 22 if manager.prompt else 0
        panel_height = prompt_height + row_height * 2 + padding * 2

        panel_rect = QRectF(
            x,
            y,
            panel_width,
            panel_height,
        )

        painter.save()
        painter.setPen(self.dynamic_border_pen)
        painter.setBrush(self.dynamic_background)
        painter.drawRoundedRect(panel_rect, 5, 5)

        font = QFont(painter.font())
        font.setPointSize(9)
        painter.setFont(font)

        current_y = y + padding

        if manager.prompt:
            painter.setPen(QColor(210, 220, 230))
            painter.drawText(
                QRectF(
                    x + padding,
                    current_y,
                    panel_width - padding * 2,
                    prompt_height,
                ),
                Qt.AlignLeft | Qt.AlignVCenter,
                manager.prompt,
            )
            current_y += prompt_height

        distance_active = (
            manager.active_mode
            == manager.MODE_DISTANCE
        )
        angle_active = (
            manager.active_mode
            == manager.MODE_ANGLE
        )

        distance_text = (
            manager.typed_value
            if distance_active and manager.typed_value
            else manager.formatted_distance()
        )

        angle_text = (
            manager.typed_value
            if angle_active and manager.typed_value
            else manager.formatted_angle()
        )

        self._draw_dynamic_row(
            painter=painter,
            x=x + padding,
            y=current_y,
            width=panel_width - padding * 2,
            height=row_height,
            label="Dist",
            value=distance_text,
            active=distance_active,
        )

        current_y += row_height

        self._draw_dynamic_row(
            painter=painter,
            x=x + padding,
            y=current_y,
            width=panel_width - padding * 2,
            height=row_height,
            label="Ang",
            value=angle_text,
            active=angle_active,
        )

        painter.restore()

    def _draw_dynamic_row(
        self,
        painter,
        x,
        y,
        width,
        height,
        label,
        value,
        active=False,
    ):
        row_rect = QRectF(
            x,
            y,
            width,
            height - 3,
        )

        painter.setPen(
            self.dynamic_active_pen
            if active
            else self.dynamic_border_pen
        )

        painter.setBrush(
            self.dynamic_active_background
            if active
            else self.dynamic_inactive_background
        )

        painter.drawRoundedRect(
            row_rect,
            3,
            3,
        )

        painter.setPen(QColor(225, 232, 238))
        painter.drawText(
            QRectF(
                x + 7,
                y,
                42,
                height - 3,
            ),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"{label}:",
        )

        painter.setPen(
            QColor(255, 230, 120)
            if active
            else QColor(235, 240, 245)
        )

        painter.drawText(
            QRectF(
                x + 50,
                y,
                width - 57,
                height - 3,
            ),
            Qt.AlignRight | Qt.AlignVCenter,
            value,
        )

    def draw_grips(
        self,
        painter,
        camera,
        grips,
    ):
        if not grips:
            return
        if not isinstance(grips, (list, tuple)):
            return

        if not grips:
            return

        for grip in grips:

            screen_x, screen_y = (
                self.coordinates.world_to_screen(
                    grip.point.x,
                    grip.point.y,
                    camera,
                )
            )

            x = int(screen_x)
            y = int(screen_y)

            size = 5

            if grip.active:

                painter.setPen(
                    QPen(
                        QColor(
                            255,
                            220,
                            0,
                        ),
                        2,
                    )
                )

                painter.setBrush(
                    QColor(
                        255,
                        220,
                        0,
                    )
                )

            elif grip.hovered:

                painter.setPen(
                    QPen(
                        QColor(
                            0,
                            255,
                            255,
                        ),
                        2,
                    )
                )

                painter.setBrush(
                    QColor(
                        0,
                        255,
                        255,
                    )
                )
            

            else:

                painter.setPen(
                    QPen(
                        QColor(
                            70,
                            160,
                            255,
                        ),
                        2,
                    )
                )

                painter.setBrush(
                    QColor(
                        70,
                        160,
                    
                    255,
                )
            )

        painter.drawRect(
            x - size,
            y - size,
            size * 2,
            size * 2,
        )

    def draw_preview(
        self,
        painter,
        camera,
        preview_geometry,
    ):
        if preview_geometry is None:
            return

        preview_type = (
            preview_geometry
            .__class__.__name__
        )

        if preview_type == "Line":
            self.draw_line(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )
        elif preview_type == "CadCircle":
            self.draw_circle(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )
        elif preview_type == "CadArc":
            self.draw_arc(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )
        elif preview_type == "Wall":
            self.draw_wall(
                painter,
                camera,
                preview_geometry,
                preview=True,
            )


    def draw_wall_nodes(self, painter, camera, network, active_node_id=None):
        if network is None:
            return
        painter.save()
        for node in network.nodes:
            x, y = self.coordinates.world_to_screen(
                node.position.x, node.position.y, camera
            )
            x, y = int(x), int(y)
            active = node.node_id == active_node_id
            size = 7 if active else 5
            if active:
                painter.setPen(QPen(QColor(255, 210, 0), 2))
                painter.setBrush(QBrush(QColor(255, 210, 0, 170)))
            else:
                painter.setPen(QPen(QColor(0, 190, 255), 1))
                painter.setBrush(QBrush(QColor(0, 190, 255, 125)))
            painter.drawEllipse(x-size, y-size, size*2, size*2)
        painter.restore()

    def draw_scene(
        self,
        painter,
        camera,
        scene,
        highlighted=None,
        selected_elements=None,
    ):
        if scene is None:
            return

        # WALL NETWORK 5.0.4.3: mantiene la topología sincronizada
        # después de crear, mover, borrar, deshacer o rehacer muros.
        wall_network = WallNetwork.ensure_scene(scene)

        # ROOM 5.0.7.3: actualiza automáticamente los recintos
        # cuando cambia la geometría de WALL / WNODE.
        from engines.architectural.room_engine import RoomEngine
        RoomEngine.update_scene_rooms(scene)
        from engines.architectural.slab_engine import SlabEngine
        SlabEngine.update_scene_slabs(scene)

        if getattr(scene, "show_wall_nodes", False):
            self.draw_wall_nodes(
                painter,
                camera,
                wall_network,
                getattr(scene, "active_wall_node_id", None),
            )

        selected_elements = set(
            selected_elements or []
        )

        layer_manager = None
        dynamic_input_manager = None

        kernel = getattr(
            scene,
            "kernel",
            None,
        )

        if kernel is not None:
            layer_manager = kernel.services.get(
                "layer_manager"
            )
        candidate = kernel.services.get(
            "dynamic_input_manager"
       )

        if (
            candidate is not None
            and hasattr(
                candidate,
                "formatted_distance",
           )
        ):
           dynamic_input_manager = candidate

        visible_walls=[]
        for candidate in scene.get_elements():
            if candidate.__class__.__name__ != "Wall": continue
            layer=None
            if layer_manager is not None: layer=layer_manager.get_layer(getattr(candidate,"layer_name","0"))
            if layer is not None and not layer.visible: continue
            if getattr(candidate,"visible",True): visible_walls.append(candidate)
        self.draw_wall_network(painter,camera,visible_walls)

        for element in scene.get_elements():
            layer_name = getattr(
                element,
                "layer_name",
                "0",
            )

            layer = None

            if layer_manager is not None:
                layer = layer_manager.get_layer(
                    layer_name
                )

            if layer is not None and not layer.visible:
                continue

            geometry = getattr(
                element,
                "geometry",
                None,
            )

            is_selected = (
                element in selected_elements
            )

            is_highlighted = (
                not is_selected
                and highlighted is not None
                and highlighted == element
            )

            if element.__class__.__name__ == "Slab":
                self.draw_slab(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif element.__class__.__name__ == "Room":
                self.draw_room(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif element.__class__.__name__ == "Wall":
                if is_selected or is_highlighted:
                    self.draw_wall(painter,camera,element,highlighted=is_highlighted,selected=is_selected)

            elif (
                geometry is not None
                and geometry.__class__.__name__
                == "Line"
            ):
                self.draw_line(
                    painter,
                    camera,
                    geometry,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadPolyline"
            ):
                self.draw_polyline(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadRectangle"
            ):
                self.draw_polyline(
                    painter,
                    camera,
                    element.polyline,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadCircle"
            ):
                self.draw_circle(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

            elif (
                element.__class__.__name__
                == "CadArc"
            ):
                self.draw_arc(
                    painter,
                    camera,
                    element,
                    highlighted=is_highlighted,
                    selected=is_selected,
                )

        selection_manager = None

        if kernel is not None:
            candidate = kernel.services.get(
                "selection_manager"
            )

            if (
                candidate is not None
                and hasattr(
                    candidate,
                    "all_grips",
                )
            ):
                selection_manager = candidate

        if selection_manager is not None:
            self.draw_grips(
                painter,
                camera,
                selection_manager.all_grips(),
            )

        self.draw_dynamic_input(
            painter,
            dynamic_input_manager,
        )
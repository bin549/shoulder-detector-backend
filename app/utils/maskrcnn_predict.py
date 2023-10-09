# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 21:51:12 2021

@author: mjye
"""
import uuid
import numpy as np
import os, cv2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
import pycocotools._mask as _mask
from IPython import display
import PIL
from django.core.files.storage import default_storage

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3

cfg.MODEL.WEIGHTS = os.path.join('./model/model_final.pth')
cfg.MODEL.DEVICE = 'cpu'
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
predictor = DefaultPredictor(cfg)


def cv2_imshow(a):
    a = a.clip(0, 255).astype('uint8')
    if a.ndim == 3:
        if a.shape[2] == 4:
            a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
        else:
            a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    display.display(PIL.Image.fromarray(a))


class Point(object):
    def __init__(self, *p):
        if len(p) == 1:
            self.x, self.y = p[0][0], p[0][1]
        else:
            self.x, self.y = p[0], p[1]
        self.length = np.sqrt(self.x ** 2 + self.y ** 2)

    def __sub__(self, other):
        return Point([self.x - other.x, self.y - other.y])

    def __add__(self, other):
        return Point([self.x + other.x, self.y + other.y])

    def __mul__(self, other):
        return Point([self.x * other, self.y * other])

    def __truediv__(self, other):
        return Point([self.x / other, self.y / other])

    def __str__(self):
        return "({:4f}, {:.4f})".format(self.x, self.y)

    def __repr__(self):
        return "({:.4f}, {:.4f})".format(self.x, self.y)

    def normalize(self):
        self.x /= self.length
        self.y /= self.length
        self.length = 1
        return self

    def negative(self):
        return Point(-self.x, -self.y)

    def perp(self):
        return Point(-self.y, self.x)


def vector_cross(va, vb):
    return va.x * vb.y - vb.x * va.y


def vector_dot(va, vb):
    return va.x * vb.x + va.y * vb.y


def is_left(p, v, v0):
    v1 = [v0[0] - v[0], v0[1] - v[1]]
    v2 = [p[0] - v[0], p[1] - v[1]]
    cp = v1[0] * v2[1] - v1[1] * v2[0]
    return cp < 0


def tangent_line_to_polygon(A, B, polygons):
    x = list(polygons[::2])
    y = list(polygons[1::2])
    x = [x[-1]] + x + [x[0]]
    y = [y[-1]] + y + [y[0]]
    polygons = [Point(i, j) for i, j in zip(x, y)]
    d = A - B
    n = d.perp().normalize()
    dist = 0
    tangent_point = None
    for i in range(1, len(polygons) - 1):
        p = polygons[i]
        p1 = polygons[i - 1]
        p2 = polygons[i + 1]
        v1 = p - p1
        v2 = p - p2
        d1 = vector_dot(v1, n)
        d2 = vector_dot(v2, n)
        if d1 * d2 >= 0:
            if np.abs(vector_dot(A - p, n)) > dist:
                dist = np.abs(vector_dot(A - p, n))
                tangent_point = p
    return dist, [tangent_point + d, tangent_point - d]


def tangent_point_to_polygon(p, polygons):
    vleft = None
    vright = None
    polygon_x = list(polygons[::2])
    polygon_y = list(polygons[1::2])
    polygon_x = [polygon_x[-1]] + polygon_x + [polygon_x[0]]
    polygon_y = [polygon_y[-1]] + polygon_y + [polygon_y[0]]
    for i in range(1, len(polygon_x) - 2):
        v = [polygon_x[i], polygon_y[i]]
        vpre = [polygon_x[i - 1], polygon_y[i - 1]]
        vnext = [polygon_x[i + 1], polygon_y[i + 1]]
        if is_left(p, v, vpre) and is_left(p, v, vnext):
            if vright is None:
                vright = v
        elif not is_left(p, v, vpre) and not is_left(p, v, vnext):
            if vleft is None:
                vleft = v
        else:
            pass
    return vright, vleft


def mask_to_convex(mask):
    contours, hierarchy = cv2.findContours(mask.astype("uint8"), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(contours[-1]).flatten()
    return hull


def mask_to_polygons(mask, convex=True):
    contours, hierarchy = cv2.findContours(mask.astype("uint8"), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if convex:
        return cv2.convexHull(contours[-1]).flatten()
    else:
        return contours[-1].flatten()


def polygons_to_mask(polygons, height, width):
    rle = _mask.frPyObjects(polygons, height, width)
    rle = _mask.merge(rle)
    return _mask.decode([rle])[:, :, 0]


def top_bottom_polygon(polygon):
    x = polygon[::2]
    y = polygon[1::2]
    maxindex = np.where(y == np.max(y))[0][0]
    minindex = np.where(y == np.min(y))[0][0]
    top = [x[minindex], y[minindex]]
    bottom = [x[maxindex], y[maxindex]]
    return top, bottom


def left_right_polygon(polygon):
    x = polygon[::2]
    y = polygon[1::2]
    maxindex = np.where(x == np.max(x))[0][0]
    minindex = np.where(x == np.min(x))[0][0]
    left = [x[minindex], y[minindex]]
    right = [x[maxindex], y[maxindex]]
    return left, right


def max_horizon_distance(polygons):
    A, B = top_bottom_polygon(polygons)
    A, B = Point(A), Point(B)
    M = (A + B) / 2
    n = (A - B).normalize()
    polygon_x = list(polygons[::2])
    polygon_y = list(polygons[1::2])
    polygon_x = [polygon_x[-1]] + polygon_x + [polygon_x[0]]
    polygon_y = [polygon_y[-1]] + polygon_y + [polygon_y[0]]
    DE = []
    for i in range(1, len(polygon_x) - 2):
        p1 = Point(polygon_x[i], polygon_y[i])
        p2 = Point(polygon_x[i + 1], polygon_y[i + 1])
        v1 = p1 - M;
        v2 = p2 - M;
        d1 = vector_dot(v1, n)
        d2 = vector_dot(v2, n)
        if np.abs(d1) < 1e-10:
            DE.append(p1)
        if np.abs(d2) < 1e-10:
            DE.append(p2)
        if np.abs(d1) > 1e-10 and np.abs(d2) > 1e-10 and d1 * d2 <= 0:
            k = np.abs(d1) / (np.abs(d1) + np.abs(d2))
            DE.append(p1 + (p2 - p1) / (1 / k))
        if len(DE) == 2:
            break
    D = [DE[0].x, DE[0].y]
    E = [DE[1].x, DE[1].y]
    return D, E


def csa_angle(predictions):
    classes = predictions.pred_classes.tolist()
    key_points = []
    masks = np.asarray(predictions.pred_masks)
    if len(masks) != 3:
        return None, None
    polygon_glenoid = mask_to_polygons(masks[classes.index(0)])
    polygon_acromion = mask_to_polygons(masks[classes.index(1)])
    A, B = top_bottom_polygon(polygon_glenoid)
    D, E = max_horizon_distance(mask_to_polygons(masks[classes.index(0)], False))[:]
    vright, vleft = tangent_point_to_polygon(B, polygon_acromion)
    key_points.extend(A)
    key_points.extend(B)
    if (max(polygon_acromion[::2]) + min(polygon_acromion[::2])) / 2 < (A[0] + B[0]) / 2:
        C = vleft
    else:
        C = vright
    key_points.extend(C)
    v1 = np.array([A[0] - B[0], A[1] - B[1]])
    v2 = np.array([C[0] - B[0], C[1] - B[1]])
    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    angle = np.degrees(angle)
    key_points.extend(D)
    key_points.extend(E)
    return key_points, angle


def tangent_distance(predictions):
    classes = predictions.pred_classes.tolist()
    masks = np.asarray(predictions.pred_masks)
    if len(masks) != 3:
        return None, None
    polygon_glenoid = mask_to_polygons(masks[classes.index(0)])
    polygon_acromion = mask_to_polygons(masks[classes.index(1)])
    polygon_humerus = mask_to_polygons(masks[classes.index(2)])
    A, B = top_bottom_polygon(polygon_glenoid)
    A, B = Point(A), Point(B)
    GA, CD = tangent_line_to_polygon(A, B, polygon_acromion)
    GH, EF = tangent_line_to_polygon(A, B, polygon_humerus)
    C, D = CD
    E, F = EF
    key_points = [A, B, C, D, E, F]
    dist = [GA, GH]
    return key_points, dist


def single_process_csa(image_file):
    im = cv2.imread(image_file)
    outputs = predictor(im)
    cv2_imshow(im)
    predictions = outputs["instances"].to("cpu")
    key_points, angle = csa_angle(predictions)
    v = Visualizer(im[:, :, ::-1],
                   scale=1.0,
                   instance_mode=ColorMode.IMAGE_BW
                   )
    out = v.draw_line(key_points[:6:2], key_points[1:6:2], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_line(key_points[6:10:2], key_points[7:10:2], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_text(np.around(angle, 2), (key_points[2], key_points[3] + 10))
    out = v.draw_instance_predictions(predictions)
    image_obj = out.get_image()[:, :, ::-1]
    # cv2_imshow(image_obj)
    file_name = str(uuid.uuid1()) + ".png"
    cv2.imwrite("./images/outputs/" + file_name, image_obj)
    return file_name


def single_process(image_file):
    im = cv2.imread(image_file)
    outputs = predictor(im)
    predictions = outputs["instances"].to("cpu")
    # key_points, angle = csa_angle(predictions)
    key_points, dist = tangent_distance(predictions)
    A, B, C, D, E, F = key_points
    v = Visualizer(im[:, :, ::-1],
                   scale=1.0,
                   instance_mode=ColorMode.IMAGE_BW
                   )

    CD1 = (C + D) / 2
    EF1 = (E + F) / 2
    if A.x < F.x:
        CD2 = CD1 - (A - B).perp().normalize() * dist[0]
        EF2 = EF1 - (A - B).perp().normalize() * dist[1]
    else:
        CD2 = CD1 + (A - B).perp().normalize() * dist[0]
        EF2 = EF1 + (A - B).perp().normalize() * dist[1]
    d1 = f"{dist[0]:.4f}"
    d2 = f"{dist[1]:.4f}"
    out = v.draw_line([A.x, B.x], [A.y, B.y], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_line([C.x, D.x], [C.y, D.y], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_line([CD1.x, CD2.x], [CD1.y, CD2.y], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_line([E.x, F.x], [E.y, F.y], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_line([EF1.x, EF2.x], [EF1.y, EF2.y], color=(1, 0, 0), linewidth=0.1)
    out = v.draw_text(d1, [((CD1 + CD2) / 2).x, ((CD1 + CD2) / 2).y])
    out = v.draw_text(d2, [((EF1 + EF2) / 2).x, ((EF1 + EF2) / 2).y])
    out = v.draw_instance_predictions(predictions)
    image_obj = out.get_image()[:, :, ::-1]
    file_name = str(uuid.uuid1()) + ".png"
    cv2.imwrite("./images/outputs/" + file_name, image_obj)
    return file_name


def main(filename):
    return single_process("./images/" + filename)


if __name__ == "__main__":
    single_process_csa('JI130705DR1053_1_10001.png')

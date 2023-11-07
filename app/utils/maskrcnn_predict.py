# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 21:51:12 2021

@author: mjye
"""
import uuid
import numpy as np
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
import pycocotools._mask as _mask
from IPython import display
import PIL
from django.core.files.storage import default_storage


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



def vector_dot(va, vb):
    return va.x * vb.x + va.y * vb.y


def is_left(p, v, v0):
    v1 = [v0[0] - v[0], v0[1] - v[1]]
    v2 = [p[0] - v[0], p[1] - v[1]]
    cp = v1[0] * v2[1] - v1[1] * v2[0]
    return cp < 0


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


def mask_to_polygons(mask, convex=True):
    contours, hierarchy = cv2.findContours(mask.astype("uint8"), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if convex:
        return cv2.convexHull(contours[-1]).flatten()
    else:
        return contours[-1].flatten()


def top_bottom_polygon(polygon):
    x = polygon[::2]
    y = polygon[1::2]
    maxindex = np.where(y == np.max(y))[0][0]
    minindex = np.where(y == np.min(y))[0][0]
    top = [x[minindex], y[minindex]]
    bottom = [x[maxindex], y[maxindex]]
    return top, bottom


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


def single_process_csa(predictor, image_file):
    im = cv2.imread(image_file)
    outputs = predictor(im)
    cv2_imshow(im)
    predictions = outputs["instances"].to("cpu")
    v = Visualizer(im[:, :, ::-1],
                   scale=1.0,
                   instance_mode=ColorMode.IMAGE_BW
                   )
    out = v.draw_instance_predictions(predictions)
    image_obj = out.get_image()[:, :, ::-1]
    file_name = str(uuid.uuid1()) + ".png"
    cv2.imwrite("./images/outputs/" + file_name, image_obj)
    return file_name


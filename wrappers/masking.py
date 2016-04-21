#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           gamera-rodan
# Program Description:    Job wrappers that allows some Gamrea functionality to work in Rodan.
#
# Filename:               gamera-rodan/wrappers/masking.py
# Purpose:                Wrapper for simple masking operations.
#
# Copyright (C) 2016 DDMAL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

import gamera
from gamera.core import Image, load_image
from rodan.jobs.base import RodanTask

import logging
logger = logging.getLogger('rodan')

class gamera_masking(RodanTask):

    name = 'Mask (logical \'and\')'
    author = 'Ryan Bannon'
    description = Image.and_image.__doc__.replace("\\n", "\n").replace('\\"', '"')
    settings ={}
    enabled = True
    category = 'Masking'
    interactive = False

    input_port_types = [{
        'name': 'Source image',
        'resource_types': ['image/rgb+png', 'image/onebit+png', 'image/greyscale+png', 'image/grey16+png'],
        'minimum': 1,
        'maximum': 1
    },
    {
        'name': 'Mask image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'Source image with mask applied',
        'resource_types': ['image/rgb+png', 'image/onebit+png', 'image/greyscale+png', 'image/grey16+png'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        image_source = load_image(inputs['Source image'][0]['resource_path'])
        image_mask = load_image(inputs['Mask image'][0]['resource_path'])
        image_result = image_source.and_image(image_mask)
        image_result.save_PNG(outputs['Source image with mask applied'][0]['resource_path'])
        return True

class gamera_gatos_threshold(RodanTask):

    name = 'Gatos Threshold'
    author = 'Ryan Bannon'
    description = gamera.plugins.binarization.gatos_threshold.escape_docstring().replace("\\n", "\n").replace('\\"', '"')
    settings = {
        'title': 'Gatos threshold settings',
        'type': 'object',
        'properties': {
            'q': {
                'type': 'number',
                'default': 0.6,
                'description': 'Use default setting (unless you know what you are doing).'
            },
            'p1': {
                'type': 'number',
                'default': 0.5,
                'description': 'Use default setting (unless you know what you are doing).' 
            },
            'p2': {
                'type': 'number',
                'default': 0.8,
                'description': 'Use default setting (unless you know what you are doing).'
            }
        }
    }

    enabled = True
    category = "Binarization"
    interactive = False

    input_port_types = [{
        'name': 'Onebit PNG - preliminary binarization of the image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    },
    {
	'name': 'Greyscale PNG - estimated background of the image',
	'resource_types': ['image/greyscale+png'],
	'minimum': 1,
	'maximum': 1
    },
    {
	'name': 'Greyscale PNG - source image to binarize',
	'resource_types': ['image/greyscale+png'],
	'minimum': 1,
	'maximum': 1
    }]
    output_port_types = [{
        'name': 'Onebit PNG - binarized image',
        'resource_types': ['image/onebit+png'],
        'minimum': 1,
        'maximum': 1
    }]

    def run_my_task(self, inputs, settings, outputs):

        image_source = load_image(inputs['Greyscale PNG - source image to binarize'][0]['resource_path'])
        image_background = load_image(inputs['Greyscale PNG - estimated background of the image'][0]['resource_path'])
	image_prelim = load_image(inputs['Onebit PNG - preliminary binarization of the image'][0]['resource_path'])
	image_result = image_source.gatos_threshold(image_background, image_prelim, settings['q'], settings['p1'], settings['p2']) 
	image_result.save_PNG(outputs['Onebit PNG - binarized image'][0]['resource_path'])
        return True
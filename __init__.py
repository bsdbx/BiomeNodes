# pylint: disable=invalid-name

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from BiomeNodes.core import register as registration_system
from BiomeNodes.core import test

bl_info = {
    'name': 'BiomeNodes',
    'description': 'Parametric node-based system for procedural biome generation.',
    'author': 'bsdbx',
    'version': (0, 0, 1),
    'blender': (3, 4, 1),
    'location': 'Node Editor',
    'warning': '',
    'doc_url': '',
    'tracker_url': '',
    'support': 'COMMUNITY',
    'category': 'Node',
}


def register() -> None:
    registration_system.reg()
    bpy.utils.register_class(test.PT_something)


def unregister() -> None:
    bpy.utils.unregister_class(test.PT_something)
    registration_system.unreg()

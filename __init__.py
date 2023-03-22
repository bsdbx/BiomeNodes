# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from .core.register import op_auto_reg

bl_info = {
    "name" : "BiomeNodes",
    "author" : "BiomeNodes",
    "description" : "",
    "blender" : (3, 5, 0),
    "version" : (0, 0, 2),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

ar_op = op_auto_reg.AutoRegisterOperators(op_auto_reg.__name__)

def register() -> None:
    ar_op.auto_register()

def unregister() -> None:
    ar_op.auto_unregister()
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""The compatible tensorflow library."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.compat.v2 import *  # pylint:disable=wildcard-import, g-bad-import-order

# Import of v1 symbols will be removed when all symbols are migrated to v2
# and tf.compat.v1. So after the migration only v2 symbols and some tf.compat.v1
# symbols are used in the codebase.
from tensorflow.compat.v1 import *  # pylint:disable=wildcard-import

# Import absl.flags and absl.logging to overwrite the Tensorflow ones.
# This is the intended behavior in TF 2.0.
# pylint:disable=g-bad-import-order, unused-import, g-import-not-at-top
from absl import flags
from absl import logging
# pylint: disable=g-direct-tensorflow-import
from tensorflow.python import tf2
from tensorflow.python.compat import v2_compat

from tensorflow.python.framework import function as _function_lib
from tensorflow.python.ops import functional_ops
from tensorflow.python.ops import inplace_ops

# The following imports are needed to expose private _Send/_Recv ops
# on TensorFlow 1.X. The could be removed once support for 1.X is dropped.
from google.protobuf import text_format as _text_format
from tensorflow.core.framework import op_def_pb2 as _op_def_pb2
from tensorflow.python.framework import op_def_library as _op_def_library
from tensorflow.python.framework import op_def_registry as _op_def_registry
# pylint: enable=g-direct-tensorflow-import

_force_disable_v2 = True
if _force_disable_v2:
  v2_compat.disable_v2_behavior()
elif tf2.enabled():
  logging.warning("Lingvo does not support TF2 yet. "
                  "Please disable V2 behavior with tf.disable_v2_behavior(), "
                  "or proceed at your own risk.")

# Aliases to a few routines lingvo libraries uses often.
Defun = _function_lib.Defun
While = functional_ops.While
If = functional_ops.If
InplaceUpdate = inplace_ops.alias_inplace_update
Empty = inplace_ops.empty
EmptyLike = inplace_ops.empty_like
GetExtraInputs = _function_lib.get_extra_inputs
GetExtraArgs = _function_lib.get_extra_args
# V1 symbols used in the codebase, and can be migrated to the v2 version later.
# pylint: disable=undefined-variable
variable_scope = tf.compat.v1.variable_scope
get_variable = tf.compat.v1.get_variable
get_variable_scope = tf.compat.v1.get_variable_scope
train.get_or_create_global_step = tf.compat.v1.train.get_or_create_global_step
train.get_global_step = tf.compat.v1.train.get_global_step
where = tf.compat.v1.where
get_collection = tf.compat.v1.get_collection
global_variables_initializer = tf.compat.v1.global_variables_initializer
assign = tf.compat.v1.assign
trainable_variables = tf.compat.v1.trainable_variables
set_random_seed = tf.compat.v1.set_random_seed
resource_loader = tf.compat.v1.resource_loader
train.Optimizer = tf.compat.v1.train.Optimizer
test.get_temp_dir = tf.compat.v1.test.get_temp_dir
test.mock = tf.compat.v1.test.mock
Session = tf.compat.v1.Session
gfile = tf.compat.v1.gfile
summary.FileWriter = tf.compat.v1.summary.FileWriter
container = tf.compat.v1.container
device = tf.compat.v1.device
get_default_graph = tf.compat.v1.get_default_graph
Dimension = tf.compat.v1.Dimension

# pylint: enable=undefined-variable


# TODO(slebedev): Remove after there is no need to support 1.X.
def _InitOpDefLibrary():
  op_list = _op_def_pb2.OpList()
  _text_format.Merge(_InitOpDefLibrary.op_list_ascii, op_list)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib


_InitOpDefLibrary.op_list_ascii = """\
op {
  name: "_Recv"
  output_arg {
    name: "tensor"
    type_attr: "tensor_type"
  }
  attr {
    name: "tensor_type"
    type: "type"
  }
  attr {
    name: "tensor_name"
    type: "string"
  }
  attr {
    name: "send_device"
    type: "string"
  }
  attr {
    name: "send_device_incarnation"
    type: "int"
  }
  attr {
    name: "recv_device"
    type: "string"
  }
  attr {
    name: "client_terminated"
    type: "bool"
    default_value {
      b: false
    }
  }
  is_stateful: true
}
op {
  name: "_Send"
  input_arg {
    name: "tensor"
    type_attr: "T"
  }
  attr {
    name: "T"
    type: "type"
  }
  attr {
    name: "tensor_name"
    type: "string"
  }
  attr {
    name: "send_device"
    type: "string"
  }
  attr {
    name: "send_device_incarnation"
    type: "int"
  }
  attr {
    name: "recv_device"
    type: "string"
  }
  attr {
    name: "client_terminated"
    type: "bool"
    default_value {
      b: false
    }
  }
  is_stateful: true
}
"""


def _Recv(tensor_type,
          tensor_name,
          send_device,
          send_device_incarnation,
          recv_device,
          name=None):
  return _op_def_lib.apply_op(
      "_Recv",
      tensor_type=tensor_type,
      tensor_name=tensor_name,
      send_device=send_device,
      send_device_incarnation=send_device_incarnation,
      recv_device=recv_device,
      client_terminated=False,
      name=name if name else "Recv")


def _Send(tensor,
          tensor_name,
          send_device,
          send_device_incarnation,
          recv_device,
          name=None):
  return _op_def_lib.apply_op(
      "_Send",
      tensor=tensor,
      tensor_name=tensor_name,
      send_device=send_device,
      send_device_incarnation=send_device_incarnation,
      recv_device=recv_device,
      client_terminated=False,
      name=name if name else "Send")


# pylint: disable=undefined-variable
if not hasattr(raw_ops, "Send") and not hasattr(raw_ops, "Recv"):
  _op_def_lib = _InitOpDefLibrary()
  raw_ops.Send = _Send
  raw_ops.Recv = _Recv
# pylint: enable=undefined-variable

del _Send, _Recv, _InitOpDefLibrary
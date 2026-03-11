// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "single_robo_custom_interface/msg/detail/cluster_points__rosidl_typesupport_introspection_c.h"
#include "single_robo_custom_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "single_robo_custom_interface/msg/detail/cluster_points__functions.h"
#include "single_robo_custom_interface/msg/detail/cluster_points__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  single_robo_custom_interface__msg__ClusterPoints__init(message_memory);
}

void single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_fini_function(void * message_memory)
{
  single_robo_custom_interface__msg__ClusterPoints__fini(message_memory);
}

size_t single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__size_function__ClusterPoints__points_arr(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_const_function__ClusterPoints__points_arr(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_function__ClusterPoints__points_arr(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__fetch_function__ClusterPoints__points_arr(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_const_function__ClusterPoints__points_arr(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__assign_function__ClusterPoints__points_arr(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_function__ClusterPoints__points_arr(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_member_array[1] = {
  {
    "points_arr",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(single_robo_custom_interface__msg__ClusterPoints, points_arr),  // bytes offset in struct
    NULL,  // default value
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__size_function__ClusterPoints__points_arr,  // size() function pointer
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_const_function__ClusterPoints__points_arr,  // get_const(index) function pointer
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__get_function__ClusterPoints__points_arr,  // get(index) function pointer
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__fetch_function__ClusterPoints__points_arr,  // fetch(index, &value) function pointer
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__assign_function__ClusterPoints__points_arr,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_members = {
  "single_robo_custom_interface__msg",  // message namespace
  "ClusterPoints",  // message name
  1,  // number of fields
  sizeof(single_robo_custom_interface__msg__ClusterPoints),
  single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_member_array,  // message members
  single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_init_function,  // function to initialize message memory (memory has to be allocated)
  single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_type_support_handle = {
  0,
  &single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_single_robo_custom_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, single_robo_custom_interface, msg, ClusterPoints)() {
  if (!single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_type_support_handle.typesupport_identifier) {
    single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &single_robo_custom_interface__msg__ClusterPoints__rosidl_typesupport_introspection_c__ClusterPoints_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
